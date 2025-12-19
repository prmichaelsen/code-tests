# User Data Architecture with Cloudflare KV

## Overview
A proper user-centric architecture using Cloudflare KV as the primary storage with anonymous user identification. Provides persistent starred locations and proper sharing functionality.

---

## Architecture Decision: KV as Primary Storage

### ✅ Why KV Should Be Primary (Not Hybrid):

1. **Persistent Across Devices** - User's starred locations available anywhere
2. **True Sharing** - Share actual data, not just IDs
3. **Simpler Architecture** - One source of truth
4. **Professional** - Real backend, not just localStorage hack
5. **Scalable** - Can add features (analytics, recommendations)

### ❌ Why localStorage Hybrid is Problematic:

1. **Not truly shareable** - Recipient gets different data than sharer
2. **Device-locked** - Can't access starred locations on different device
3. **Complex sync** - Need to sync between localStorage and KV
4. **Inconsistent** - Two sources of truth
5. **Limited** - Can't add server-side features

---

## User Identification Strategy

### Anonymous User ID (No Auth Required)

```typescript
/**
 * Generate or retrieve anonymous user ID
 * Stored in localStorage, used to identify user in KV
 */
function getUserId(): string {
  const STORAGE_KEY = 'map-search-user-id';
  
  let userId = localStorage.getItem(STORAGE_KEY);
  
  if (!userId) {
    // Generate UUID for anonymous user
    userId = crypto.randomUUID();
    localStorage.setItem(STORAGE_KEY, userId);
  }
  
  return userId;
}
```

**Benefits:**
- ✅ No authentication required
- ✅ Persistent across sessions (same browser)
- ✅ Unique per user
- ✅ Can track user's starred locations
- ✅ Simple to implement

---

## Cloudflare KV Data Structure

### User Data Storage

```typescript
// KV Key: `user:{userId}`
// KV Value:
{
  userId: "550e8400-e29b-41d4-a716-446655440000",
  starredLocationIds: [1, 3, 5, 7],
  createdAt: 1703001234567,
  updatedAt: 1703001234567
}

// KV Key: `share:{shareId}`
// KV Value:
{
  shareId: "abc123",
  userId: "550e8400-e29b-41d4-a716-446655440000",
  locationIds: [1, 3, 5],
  createdAt: 1703001234567,
  expiresAt: 1705593234567
}
```

---

## Proper Abstractions

### 1. Custom Hook: useUser

**File: `src/hooks/useUser.ts`**

```typescript
import { useState, useEffect, useCallback } from 'react';

export interface User {
  id: string;
  isAnonymous: boolean;
}

export function useUser() {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    // Get or create user ID
    const userId = getUserId();
    setUser({
      id: userId,
      isAnonymous: true,
    });
  }, []);

  const resetUser = useCallback(() => {
    localStorage.removeItem('map-search-user-id');
    const newUserId = getUserId();
    setUser({
      id: newUserId,
      isAnonymous: true,
    });
  }, []);

  return { user, resetUser };
}

function getUserId(): string {
  const STORAGE_KEY = 'map-search-user-id';
  let userId = localStorage.getItem(STORAGE_KEY);
  
  if (!userId) {
    userId = crypto.randomUUID();
    localStorage.setItem(STORAGE_KEY, userId);
  }
  
  return userId;
}
```

### 2. Custom Hook: useStarredLocations

**File: `src/hooks/useStarredLocations.ts`**

```typescript
import { useState, useEffect, useCallback } from 'react';
import { useUser } from './useUser';
import * as starService from '../services/starService';

export function useStarredLocations() {
  const { user } = useUser();
  const [starredIds, setStarredIds] = useState<number[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Load starred locations from KV
  useEffect(() => {
    if (!user) return;

    const loadStarred = async () => {
      try {
        const ids = await starService.fetchStarredLocationIds(user.id);
        setStarredIds(ids);
      } catch (error) {
        console.error('Failed to load starred locations:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadStarred();
  }, [user]);

  const toggleStar = useCallback(async (locationId: number) => {
    if (!user) return;

    const isCurrentlyStarred = starredIds.includes(locationId);
    
    // Optimistic update
    setStarredIds(prev =>
      isCurrentlyStarred
        ? prev.filter(id => id !== locationId)
        : [...prev, locationId]
    );

    try {
      await starService.toggleStar(user.id, locationId);
    } catch (error) {
      // Rollback on error
      setStarredIds(prev =>
        isCurrentlyStarred
          ? [...prev, locationId]
          : prev.filter(id => id !== locationId)
      );
      console.error('Failed to toggle star:', error);
      throw error;
    }
  }, [user, starredIds]);

  const isStarred = useCallback((locationId: number) => {
    return starredIds.includes(locationId);
  }, [starredIds]);

  return {
    starredIds,
    isStarred,
    toggleStar,
    starredCount: starredIds.length,
    isLoading,
  };
}
```

### 3. Custom Hook: useShare

**File: `src/hooks/useShare.ts`**

```typescript
import { useState, useCallback } from 'react';
import { useUser } from './useUser';
import * as shareService from '../services/shareService';

export function useShare() {
  const { user } = useUser();
  const [shareUrl, setShareUrl] = useState<string>('');
  const [isSharing, setIsSharing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createShare = useCallback(async (locationIds: number[]) => {
    if (!user) {
      throw new Error('User not initialized');
    }

    setIsSharing(true);
    setError(null);

    try {
      const result = await shareService.createSharedList(user.id, locationIds);
      setShareUrl(result.url);
      
      // Copy to clipboard
      await navigator.clipboard.writeText(result.url);
      
      return result;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to create share';
      setError(message);
      throw err;
    } finally {
      setIsSharing(false);
    }
  }, [user]);

  const loadShare = useCallback(async (shareId: string) => {
    try {
      return await shareService.getSharedList(shareId);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to load share';
      setError(message);
      throw err;
    }
  }, []);

  const clearShare = useCallback(() => {
    setShareUrl('');
    setError(null);
  }, []);

  return {
    shareUrl,
    isSharing,
    error,
    createShare,
    loadShare,
    clearShare,
  };
}
```

---

## Service Layer with Proper Abstractions

### File: `src/services/starService.ts`

```typescript
import { z } from 'zod';

const API_URL = import.meta.env.VITE_API_URL || '/api';

const UserStarDataSchema = z.object({
  userId: z.string().uuid(),
  starredLocationIds: z.array(z.number().int().positive()),
  updatedAt: z.number().int().positive(),
});

type UserStarData = z.infer<typeof UserStarDataSchema>;

/**
 * Fetch user's starred location IDs from KV
 */
export async function fetchStarredLocationIds(userId: string): Promise<number[]> {
  const response = await fetch(`${API_URL}/users/${userId}/starred`);
  
  if (response.status === 404) {
    return []; // User has no starred locations yet
  }
  
  if (!response.ok) {
    throw new Error('Failed to fetch starred locations');
  }

  const data = await response.json();
  const validated = UserStarDataSchema.parse(data);
  return validated.starredLocationIds;
}

/**
 * Toggle star status for a location
 */
export async function toggleStar(userId: string, locationId: number): Promise<UserStarData> {
  const response = await fetch(`${API_URL}/users/${userId}/starred/${locationId}`, {
    method: 'POST',
  });

  if (!response.ok) {
    throw new Error('Failed to toggle star');
  }

  const data = await response.json();
  return UserStarDataSchema.parse(data);
}

/**
 * Star multiple locations (for loading shared lists)
 */
export async function starMultiple(userId: string, locationIds: number[]): Promise<UserStarData> {
  const response = await fetch(`${API_URL}/users/${userId}/starred/bulk`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ locationIds }),
  });

  if (!response.ok) {
    throw new Error('Failed to star locations');
  }

  const data = await response.json();
  return UserStarDataSchema.parse(data);
}
```

### File: `src/services/shareService.ts`

```typescript
import { z } from 'zod';

const API_URL = import.meta.env.VITE_API_URL || '/api';

const SharedListResponseSchema = z.object({
  shareId: z.string().length(8),
  url: z.string().url(),
  expiresAt: z.number().int().positive(),
});

const SharedListDataSchema = z.object({
  shareId: z.string(),
  userId: z.string().uuid(),
  locationIds: z.array(z.number().int().positive()),
  createdAt: z.number().int().positive(),
});

type SharedListResponse = z.infer<typeof SharedListResponseSchema>;
type SharedListData = z.infer<typeof SharedListDataSchema>;

/**
 * Create a shareable list
 */
export async function createSharedList(
  userId: string,
  locationIds: number[]
): Promise<SharedListResponse> {
  const response = await fetch(`${API_URL}/share`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ userId, locationIds }),
  });

  if (!response.ok) {
    throw new Error('Failed to create shared list');
  }

  const data = await response.json();
  return SharedListResponseSchema.parse(data);
}

/**
 * Get a shared list
 */
export async function getSharedList(shareId: string): Promise<SharedListData> {
  const response = await fetch(`${API_URL}/share/${shareId}`);

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Shared list not found or expired');
    }
    throw new Error('Failed to fetch shared list');
  }

  const data = await response.json();
  return SharedListDataSchema.parse(data);
}
```

---

## Cloudflare Worker API

### File: `workers/api/src/index.ts`

```typescript
import { z } from 'zod';

export interface Env {
  USER_DATA: KVNamespace;    // User starred locations
  SHARED_LISTS: KVNamespace; // Shared lists
}

// Schemas
const UserStarDataSchema = z.object({
  userId: z.string().uuid(),
  starredLocationIds: z.array(z.number().int().positive()),
  updatedAt: z.number().int().positive(),
});

const CreateShareSchema = z.object({
  userId: z.string().uuid(),
  locationIds: z.array(z.number().int().positive()).min(1).max(50),
});

const SharedListDataSchema = z.object({
  shareId: z.string(),
  userId: z.string().uuid(),
  locationIds: z.array(z.number().int().positive()),
  createdAt: z.number().int().positive(),
});

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    try {
      // GET /api/users/:userId/starred - Get user's starred locations
      if (url.pathname.match(/^\/api\/users\/[^/]+\/starred$/) && request.method === 'GET') {
        const userId = url.pathname.split('/')[3];
        
        const data = await env.USER_DATA.get(`user:${userId}`);
        
        if (!data) {
          // User has no starred locations yet
          return new Response(
            JSON.stringify({ userId, starredLocationIds: [], updatedAt: Date.now() }),
            { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
          );
        }

        return new Response(data, {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      }

      // POST /api/users/:userId/starred/:locationId - Toggle star
      if (url.pathname.match(/^\/api\/users\/[^/]+\/starred\/\d+$/) && request.method === 'POST') {
        const parts = url.pathname.split('/');
        const userId = parts[3];
        const locationId = parseInt(parts[5]);

        // Get current starred locations
        const existing = await env.USER_DATA.get(`user:${userId}`);
        let userData = existing
          ? UserStarDataSchema.parse(JSON.parse(existing))
          : { userId, starredLocationIds: [], updatedAt: Date.now() };

        // Toggle star
        const index = userData.starredLocationIds.indexOf(locationId);
        if (index > -1) {
          userData.starredLocationIds.splice(index, 1); // Unstar
        } else {
          userData.starredLocationIds.push(locationId); // Star
        }

        userData.updatedAt = Date.now();

        // Save back to KV
        await env.USER_DATA.put(
          `user:${userId}`,
          JSON.stringify(userData)
        );

        return new Response(JSON.stringify(userData), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      }

      // POST /api/users/:userId/starred/bulk - Star multiple
      if (url.pathname.match(/^\/api\/users\/[^/]+\/starred\/bulk$/) && request.method === 'POST') {
        const userId = url.pathname.split('/')[3];
        const { locationIds } = await request.json();

        // Get current starred locations
        const existing = await env.USER_DATA.get(`user:${userId}`);
        let userData = existing
          ? UserStarDataSchema.parse(JSON.parse(existing))
          : { userId, starredLocationIds: [], updatedAt: Date.now() };

        // Add new starred locations (avoid duplicates)
        const newIds = locationIds.filter((id: number) => !userData.starredLocationIds.includes(id));
        userData.starredLocationIds.push(...newIds);
        userData.updatedAt = Date.now();

        // Save back to KV
        await env.USER_DATA.put(
          `user:${userId}`,
          JSON.stringify(userData)
        );

        return new Response(JSON.stringify(userData), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      }

      // POST /api/share - Create shared list
      if (url.pathname === '/api/share' && request.method === 'POST') {
        const body = await request.json();
        const { userId, locationIds } = CreateShareSchema.parse(body);

        const shareId = crypto.randomUUID().slice(0, 8);
        
        const sharedList = {
          shareId,
          userId,
          locationIds,
          createdAt: Date.now(),
        };

        const validated = SharedListDataSchema.parse(sharedList);

        // Store in KV with 30-day expiration
        await env.SHARED_LISTS.put(
          `share:${shareId}`,
          JSON.stringify(validated),
          { expirationTtl: 60 * 60 * 24 * 30 }
        );

        return new Response(
          JSON.stringify({
            shareId,
            url: `${url.origin}/shared/${shareId}`,
            expiresAt: Date.now() + (60 * 60 * 24 * 30 * 1000),
          }),
          { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
        );
      }

      // GET /api/share/:id - Get shared list
      if (url.pathname.startsWith('/api/share/') && request.method === 'GET') {
        const shareId = url.pathname.split('/').pop();
        
        if (!shareId) {
          return new Response('Invalid share ID', { status: 400, headers: corsHeaders });
        }

        const data = await env.SHARED_LISTS.get(`share:${shareId}`);
        
        if (!data) {
          return new Response(
            JSON.stringify({ error: 'Shared list not found or expired' }),
            { status: 404, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
          );
        }

        const validated = SharedListDataSchema.parse(JSON.parse(data));

        return new Response(JSON.stringify(validated), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      }

      return new Response('Not Found', { status: 404, headers: corsHeaders });
      
    } catch (error) {
      if (error instanceof z.ZodError) {
        return new Response(
          JSON.stringify({ error: 'Validation error', details: error.errors }),
          { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
        );
      }
      
      console.error('Worker error:', error);
      return new Response('Internal Server Error', {
        status: 500,
        headers: corsHeaders,
      });
    }
  },
};
```

---

## Updated Component with Proper Abstractions

### File: `src/components/Share/ShareButton.tsx`

```typescript
import React, { useState, useCallback } from 'react';
import { useStarredLocations } from '@hooks/useStarredLocations';
import { useShare } from '@hooks/useShare';

const ShareButton: React.FC = () => {
  const { starredIds, starredCount } = useStarredLocations();
  const { shareUrl, isSharing, error, createShare, clearShare } = useShare();
  const [copied, setCopied] = useState(false);

  const handleShare = useCallback(async () => {
    try {
      await createShare(starredIds);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      // Error already handled in useShare hook
      console.error('Share failed:', error);
    }
  }, [starredIds, createShare]);

  if (starredCount === 0) {
    return null;
  }

  return (
    <div className="share-container">
      <button
        onClick={handleShare}
        disabled={isSharing}
        className="share-button"
      >
        {isSharing ? 'Creating link...' : `Share ${starredCount} Starred`}
      </button>
      
      {copied && (
        <span className="share-success">✓ Link copied!</span>
      )}
      
      {error && (
        <span className="share-error">{error}</span>
      )}
      
      {shareUrl && (
        <input
          type="text"
          value={shareUrl}
          readOnly
          onClick={(e) => e.currentTarget.select()}
          className="share-url-input"
        />
      )}
    </div>
  );
};

export default ShareButton;
```

### File: `src/components/Star/StarButton.tsx`

```typescript
import React, { useCallback } from 'react';
import { useStarredLocations } from '@hooks/useStarredLocations';

interface StarButtonProps {
  locationId: number;
  className?: string;
}

const StarButton: React.FC<StarButtonProps> = ({ locationId, className }) => {
  const { isStarred, toggleStar } = useStarredLocations();
  const starred = isStarred(locationId);

  const handleClick = useCallback(async (e: React.MouseEvent) => {
    e.stopPropagation();
    
    try {
      await toggleStar(locationId);
    } catch (error) {
      console.error('Failed to toggle star:', error);
      alert('Failed to update favorite status');
    }
  }, [locationId, toggleStar]);

  return (
    <button
      onClick={handleClick}
      className={`star-button ${starred ? 'starred' : ''} ${className || ''}`}
      aria-label={starred ? 'Remove from favorites' : 'Add to favorites'}
      title={starred ? 'Remove from favorites' : 'Add to favorites'}
    >
      <span className="star-icon">{starred ? '★' : '☆'}</span>
    </button>
  );
};

export default StarButton;
```

---

## Data Flow

### Starring a Location:

```
User clicks star
  ↓
StarButton → useStarredLocations.toggleStar(id)
  ↓
starService.toggleStar(userId, id)
  ↓
Worker: GET user:{userId} from KV
  ↓
Worker: Toggle ID in starredLocationIds array
  ↓
Worker: PUT user:{userId} back to KV
  ↓
Hook updates local state (optimistic)
  ↓
UI re-renders with new star status
```

### Sharing Starred Locations:

```
User clicks "Share"
  ↓
ShareButton → useShare.createShare(starredIds)
  ↓
shareService.createSharedList(userId, starredIds)
  ↓
Worker: Generate shareId "abc123"
  ↓
Worker: PUT share:abc123 to KV { userId, locationIds, createdAt }
  ↓
Worker: Return { shareId, url, expiresAt }
  ↓
Hook copies URL to clipboard
  ↓
User shares URL
```

### Loading Shared List:

```
Friend opens /shared/abc123
  ↓
App → useShare.loadShare("abc123")
  ↓
shareService.getSharedList("abc123")
  ↓
Worker: GET share:abc123 from KV
  ↓
Worker: Return { userId, locationIds, createdAt }
  ↓
App → useStarredLocations.starMultiple(locationIds)
  ↓
starService.starMultiple(friendUserId, locationIds)
  ↓
Worker: Add to friend's starred locations
  ↓
Friend sees shared locations as starred!
```

---

## Benefits of This Architecture

### ✅ Proper Abstractions:

1. **Custom Hooks** - Business logic separated from UI
2. **Service Layer** - API calls abstracted
3. **Zod Schemas** - Runtime validation everywhere
4. **User Context** - User ID management
5. **Clean Components** - Just UI, no business logic

### ✅ User Identification:

1. **Anonymous UUID** - No auth required
2. **Persistent** - Stored in localStorage
3. **Cross-device** - Can implement login later
4. **Trackable** - Can see who starred what
5. **Shareable** - Share lists between users

### ✅ KV as Primary:

1. **True Persistence** - Data survives browser clear
2. **Cross-device Ready** - Add auth later for sync
3. **Shareable** - Real sharing, not just IDs
4. **Scalable** - Can add features (analytics, recommendations)
5. **Professional** - Real backend architecture

---

## File Structure

```
src/
├── hooks/
│   ├── useUser.ts              # User ID management
│   ├── useStarredLocations.ts  # Starred locations logic
│   └── useShare.ts             # Sharing logic
├── services/
│   ├── starService.ts          # Star API calls
│   ├── shareService.ts         # Share API calls
│   └── locationService.ts      # Location CRUD
├── schemas/
│   ├── location.schema.ts      # Location validation
│   ├── user.schema.ts          # User data validation
│   └── share.schema.ts         # Share validation
└── components/
    ├── Star/
    │   └── StarButton.tsx      # Uses useStarredLocations hook
    └── Share/
        └── ShareButton.tsx     # Uses useShare hook
```

---

## Summary

### ✅ Recommended Architecture:

**Storage**: Cloudflare KV (primary)
- User starred locations: `user:{userId}`
- Shared lists: `share:{shareId}`

**User ID**: Anonymous UUID
- Generated on first visit
- Stored in localStorage
- Used for KV operations

**Abstractions**:
- `useUser()` - User management
- `useStarredLocations()` - Star operations
- `useShare()` - Share operations
- Service layer for API calls
- Zod schemas for validation

**Benefits**:
- ✅ Clean separation of concerns
- ✅ Reusable hooks
- ✅ Type-safe with Zod
- ✅ Persistent across devices (with future auth)
- ✅ True sharing functionality
- ✅ Professional architecture

This is a much better architecture than the localStorage hybrid approach!