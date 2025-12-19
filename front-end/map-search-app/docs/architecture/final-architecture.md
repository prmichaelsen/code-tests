# Final Architecture: Contexts, Services, and Schemas

## Overview
Production-ready architecture with proper separation: Contexts for state management, Services for API calls, Schemas in separate files for validation.

---

## Architecture Layers

```
┌─────────────────────────────────────────────────────────┐
│ Components (UI Only)                                    │
│ - Just render and handle user interactions              │
└─────────────────────────────────────────────────────────┘
                          ↓ uses
┌─────────────────────────────────────────────────────────┐
│ Contexts (State Management)                             │
│ - UserContext                                           │
│ - StarredLocationsContext                               │
│ - ShareContext                                          │
│ - LocationDataContext                                   │
│ - SelectedLocationContext                               │
│ - SearchContext                                         │
│ - MapInstanceContext                                    │
│ - MapStateContext                                       │
└─────────────────────────────────────────────────────────┘
                          ↓ calls
┌─────────────────────────────────────────────────────────┐
│ Services (API Layer)                                    │
│ - starService.ts                                        │
│ - shareService.ts                                       │
│ - locationService.ts                                    │
└─────────────────────────────────────────────────────────┘
                          ↓ validates with
┌─────────────────────────────────────────────────────────┐
│ Schemas (Validation - Separate Files)                  │
│ - api/*.api.schema.ts                                   │
│ - kv/*.kv.schema.ts                                     │
│ - domain/*.domain.schema.ts                             │
└─────────────────────────────────────────────────────────┘
                          ↓ calls
┌─────────────────────────────────────────────────────────┐
│ Cloudflare Worker + KV                                  │
│ - API endpoints                                         │
│ - KV storage                                            │
└─────────────────────────────────────────────────────────┘
```

---

## Context Architecture (8 Contexts)

### 1. UserContext

**File: `src/contexts/UserContext.tsx`**

```typescript
import React, { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react';

interface User {
  id: string;
  isAnonymous: boolean;
}

interface UserContextType {
  user: User | null;
  resetUser: () => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const userId = getUserId();
    setUser({ id: userId, isAnonymous: true });
  }, []);

  const resetUser = useCallback(() => {
    localStorage.removeItem('map-search-user-id');
    const newUserId = getUserId();
    setUser({ id: newUserId, isAnonymous: true });
  }, []);

  const value = { user, resetUser };

  return <UserContext.Provider value={value}>{children}</UserContext.Provider>;
};

export const useUser = () => {
  const context = useContext(UserContext);
  if (!context) throw new Error('useUser must be used within UserProvider');
  return context;
};

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

### 2. StarredLocationsContext

**File: `src/contexts/StarredLocationsContext.tsx`**

```typescript
import React, { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react';
import { useUser } from './UserContext';
import * as starService from '../services/starService';

interface StarredLocationsContextType {
  starredLocationIds: number[];
  isStarred: (id: number) => boolean;
  toggleStar: (id: number) => Promise<void>;
  starMultiple: (ids: number[]) => Promise<void>;
  starredCount: number;
  isLoading: boolean;
}

const StarredLocationsContext = createContext<StarredLocationsContextType | undefined>(undefined);

export const StarredLocationsProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const { user } = useUser();
  const [starredLocationIds, setStarredLocationIds] = useState<number[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Load starred locations from KV
  useEffect(() => {
    if (!user) return;

    const loadStarred = async () => {
      try {
        const ids = await starService.fetchStarredLocationIds(user.id);
        setStarredLocationIds(ids);
      } catch (error) {
        console.error('Failed to load starred locations:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadStarred();
  }, [user]);

  const isStarred = useCallback((id: number) => {
    return starredLocationIds.includes(id);
  }, [starredLocationIds]);

  const toggleStar = useCallback(async (locationId: number) => {
    if (!user) return;

    const wasStarred = starredLocationIds.includes(locationId);
    
    // Optimistic update
    setStarredLocationIds(prev =>
      wasStarred ? prev.filter(id => id !== locationId) : [...prev, locationId]
    );

    try {
      const response = await starService.toggleStar(user.id, locationId);
      // Update with server response
      setStarredLocationIds(response.starredLocationIds);
    } catch (error) {
      // Rollback on error
      setStarredLocationIds(prev =>
        wasStarred ? [...prev, locationId] : prev.filter(id => id !== locationId)
      );
      throw error;
    }
  }, [user, starredLocationIds]);

  const starMultiple = useCallback(async (locationIds: number[]) => {
    if (!user) return;

    try {
      const response = await starService.starMultiple(user.id, locationIds);
      setStarredLocationIds(response.starredLocationIds);
    } catch (error) {
      console.error('Failed to star multiple locations:', error);
      throw error;
    }
  }, [user]);

  const value = {
    starredLocationIds,
    isStarred,
    toggleStar,
    starMultiple,
    starredCount: starredLocationIds.length,
    isLoading,
  };

  return (
    <StarredLocationsContext.Provider value={value}>
      {children}
    </StarredLocationsContext.Provider>
  );
};

export const useStarredLocations = () => {
  const context = useContext(StarredLocationsContext);
  if (!context) throw new Error('useStarredLocations must be used within StarredLocationsProvider');
  return context;
};
```

### 3. ShareContext

**File: `src/contexts/ShareContext.tsx`**

```typescript
import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { useUser } from './UserContext';
import * as shareService from '../services/shareService';
import type { ApiCreateShareResponse } from '../schemas/api/share.api.schema';

interface ShareContextType {
  shareUrl: string;
  isSharing: boolean;
  error: string | null;
  createShare: (locationIds: number[]) => Promise<ApiCreateShareResponse>;
  loadShare: (shareId: string) => Promise<number[]>;
  clearShare: () => void;
}

const ShareContext = createContext<ShareContextType | undefined>(undefined);

export const ShareProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
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
    setError(null);
    
    try {
      const data = await shareService.getSharedList(shareId);
      return data.locationIds;
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

  const value = {
    shareUrl,
    isSharing,
    error,
    createShare,
    loadShare,
    clearShare,
  };

  return <ShareContext.Provider value={value}>{children}</ShareContext.Provider>;
};

export const useShare = () => {
  const context = useContext(ShareContext);
  if (!context) throw new Error('useShare must be used within ShareProvider');
  return context;
};
```

---

## Schema Files (Separate, Not Colocated)

### File: `src/schemas/api/star.api.schema.ts`

```typescript
import { z } from 'zod';

/**
 * API Response: GET /api/users/:userId/starred
 */
export const ApiGetStarredResponseSchema = z.object({
  userId: z.string().uuid(),
  starredLocationIds: z.array(z.number().int().positive()),
  updatedAt: z.number().int().positive(),
});

/**
 * API Response: POST /api/users/:userId/starred/:locationId
 */
export const ApiToggleStarResponseSchema = z.object({
  userId: z.string().uuid(),
  locationId: z.number().int().positive(),
  starred: z.boolean(),
  starredLocationIds: z.array(z.number().int().positive()),
  updatedAt: z.number().int().positive(),
});

/**
 * API Request: POST /api/users/:userId/starred/bulk
 */
export const ApiStarBulkRequestSchema = z.object({
  locationIds: z.array(z.number().int().positive()).min(1).max(50),
});

/**
 * API Response: POST /api/users/:userId/starred/bulk
 */
export const ApiStarBulkResponseSchema = z.object({
  userId: z.string().uuid(),
  starredLocationIds: z.array(z.number().int().positive()),
  addedCount: z.number().int().nonnegative(),
  updatedAt: z.number().int().positive(),
});

// Export types
export type ApiGetStarredResponse = z.infer<typeof ApiGetStarredResponseSchema>;
export type ApiToggleStarResponse = z.infer<typeof ApiToggleStarResponseSchema>;
export type ApiStarBulkRequest = z.infer<typeof ApiStarBulkRequestSchema>;
export type ApiStarBulkResponse = z.infer<typeof ApiStarBulkResponseSchema>;
```

### File: `src/services/starService.ts` (Uses Schemas)

```typescript
import {
  ApiGetStarredResponse,
  ApiGetStarredResponseSchema,
  ApiToggleStarResponse,
  ApiToggleStarResponseSchema,
  ApiStarBulkRequest,
  ApiStarBulkRequestSchema,
  ApiStarBulkResponse,
  ApiStarBulkResponseSchema,
} from '../schemas/api/star.api.schema';

const API_URL = import.meta.env.VITE_API_URL || '/api';

export async function fetchStarredLocationIds(userId: string): Promise<number[]> {
  const response = await fetch(`${API_URL}/users/${userId}/starred`);
  
  if (response.status === 404) {
    return [];
  }
  
  if (!response.ok) {
    throw new Error('Failed to fetch starred locations');
  }

  const data: unknown = await response.json();
  const validated: ApiGetStarredResponse = ApiGetStarredResponseSchema.parse(data);
  
  return validated.starredLocationIds;
}

export async function toggleStar(
  userId: string,
  locationId: number
): Promise<ApiToggleStarResponse> {
  const response = await fetch(`${API_URL}/users/${userId}/starred/${locationId}`, {
    method: 'POST',
  });

  if (!response.ok) {
    throw new Error('Failed to toggle star');
  }

  const data: unknown = await response.json();
  return ApiToggleStarResponseSchema.parse(data);
}

export async function starMultiple(
  userId: string,
  locationIds: number[]
): Promise<ApiStarBulkResponse> {
  // Validate request
  const request: ApiStarBulkRequest = ApiStarBulkRequestSchema.parse({ locationIds });
  
  const response = await fetch(`${API_URL}/users/${userId}/starred/bulk`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error('Failed to star locations');
  }

  const data: unknown = await response.json();
  return ApiStarBulkResponseSchema.parse(data);
}
```

---

## Updated Provider Hierarchy

### File: `src/main.tsx`

```typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

// User identification (foundational)
import { UserProvider } from './contexts/UserContext';

// Data contexts
import { LocationDataProvider } from './contexts/LocationDataContext';
import { StarredLocationsProvider } from './contexts/StarredLocationsContext';
import { ShareProvider } from './contexts/ShareContext';

// Selection contexts
import { SelectedLocationProvider } from './contexts/SelectedLocationContext';
import { SearchProvider } from './contexts/SearchContext';

// Map contexts
import { MapInstanceProvider } from './contexts/MapInstanceContext';
import { MapStateProvider } from './contexts/MapStateContext';

import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    {/* User identification - foundational */}
    <UserProvider>
      
      {/* Data layer */}
      <LocationDataProvider>
        <StarredLocationsProvider>
          <ShareProvider>
            
            {/* Map layer */}
            <MapInstanceProvider>
              <MapStateProvider>
                
                {/* Selection layer */}
                <SelectedLocationProvider>
                  <SearchProvider>
                    <App />
                  </SearchProvider>
                </SelectedLocationProvider>
                
              </MapStateProvider>
            </MapInstanceProvider>
            
          </ShareProvider>
        </StarredLocationsProvider>
      </LocationDataProvider>
      
    </UserProvider>
  </React.StrictMode>
);
```

---

## Complete File Structure

```
src/
├── schemas/                              # All schemas in separate files
│   ├── api/                              # API layer DTOs
│   │   ├── location.api.schema.ts        # Location API schemas
│   │   ├── star.api.schema.ts            # Star API schemas
│   │   └── share.api.schema.ts           # Share API schemas
│   ├── kv/                               # KV storage DTOs
│   │   ├── user.kv.schema.ts             # User KV schemas
│   │   └── share.kv.schema.ts            # Share KV schemas
│   ├── domain/                           # Domain entities
│   │   └── location.domain.schema.ts     # Core Location entity
│   ├── local/                            # localStorage DTOs
│   │   └── preferences.local.schema.ts   # User preferences
│   └── index.ts                          # Re-export all
│
├── contexts/                             # State management (8 contexts)
│   ├── UserContext.tsx                   # User identification
│   ├── StarredLocationsContext.tsx       # Starred locations state
│   ├── ShareContext.tsx                  # Sharing state
│   ├── LocationDataContext.tsx           # Locations array
│   ├── SelectedLocationContext.tsx       # Current selection
│   ├── SearchContext.tsx                 # Search state
│   ├── MapInstanceContext.tsx            # Map instance
│   └── MapStateContext.tsx               # Map center/zoom
│
├── services/                             # API calls (import schemas)
│   ├── starService.ts                    # Uses api/star.api.schema.ts
│   ├── shareService.ts                   # Uses api/share.api.schema.ts
│   └── locationService.ts                # Uses api/location.api.schema.ts
│
└── components/                           # UI (use contexts)
    ├── Star/
    │   └── StarButton.tsx                # Uses StarredLocationsContext
    └── Share/
        └── ShareButton.tsx               # Uses ShareContext

workers/api/
├── src/
│   ├── schemas/                          # Worker schemas (separate)
│   │   ├── kv.schemas.ts                 # KV storage schemas
│   │   └── api.schemas.ts                # API request/response schemas
│   └── index.ts                          # Worker implementation
└── wrangler.toml
```

---

## Component Usage (Clean and Simple)

### StarButton Component

```typescript
import React, { useCallback } from 'react';
import { useStarredLocations } from '@contexts/StarredLocationsContext';

interface StarButtonProps {
  locationId: number;
}

const StarButton: React.FC<StarButtonProps> = ({ locationId }) => {
  // ✅ Just use context, no business logic here
  const { isStarred, toggleStar } = useStarredLocations();
  const starred = isStarred(locationId);

  const handleClick = useCallback(async (e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await toggleStar(locationId);
    } catch (error) {
      console.error('Failed to toggle star:', error);
    }
  }, [locationId, toggleStar]);

  return (
    <button onClick={handleClick} className={starred ? 'starred' : ''}>
      {starred ? '★' : '☆'}
    </button>
  );
};

export default StarButton;
```

### ShareButton Component

```typescript
import React, { useState, useCallback } from 'react';
import { useStarredLocations } from '@contexts/StarredLocationsContext';
import { useShare } from '@contexts/ShareContext';

const ShareButton: React.FC = () => {
  // ✅ Just use contexts, no business logic here
  const { starredLocationIds, starredCount } = useStarredLocations();
  const { shareUrl, isSharing, error, createShare } = useShare();
  const [copied, setCopied] = useState(false);

  const handleShare = useCallback(async () => {
    try {
      await createShare(starredLocationIds);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error('Share failed:', error);
    }
  }, [starredLocationIds, createShare]);

  if (starredCount === 0) return null;

  return (
    <div>
      <button onClick={handleShare} disabled={isSharing}>
        {isSharing ? 'Creating...' : `Share ${starredCount} Starred`}
      </button>
      {copied && <span>✓ Copied!</span>}
      {error && <span>{error}</span>}
    </div>
  );
};

export default ShareButton;
```

---

## Benefits of This Architecture

### ✅ Contexts (Not Hooks):

**Why contexts are better:**
- State is shared across components
- Single source of truth
- Automatic re-renders when state changes
- Can be consumed anywhere in tree
- Standard React pattern for global state

**Hooks are for:**
- Reusable logic without state
- Composing multiple contexts
- Side effects
- Not for global state management

### ✅ Schemas in Separate Files:

**Why separate:**
- Clear organization by service layer
- Easy to find and update
- No circular dependencies
- Can be shared between client and worker
- Single source of truth for validation

**File naming makes it clear:**
```typescript
// ✅ Clear: This is an API response schema
import { ApiGetStarredResponseSchema } from '@schemas/api/star.api.schema';

// ✅ Clear: This is KV storage schema
import { KvUserStarDataSchema } from '@schemas/kv/user.kv.schema';

// ✅ Clear: This is a domain entity
import { LocationDomainSchema } from '@schemas/domain/location.domain.schema';
```

---

## Context vs Hook Decision Matrix

| Use Case | Use Context | Use Hook |
|----------|-------------|----------|
| Global state | ✅ Yes | ❌ No |
| Shared across components | ✅ Yes | ❌ No |
| Triggers re-renders | ✅ Yes | ❌ No |
| Reusable logic (no state) | ❌ No | ✅ Yes |
| Compose multiple contexts | ❌ No | ✅ Yes |
| Side effects only | ❌ No | ✅ Yes |

**Examples:**
- `UserContext` ✅ - Global user state
- `StarredLocationsContext` ✅ - Global starred state
- `ShareContext` ✅ - Global sharing state
- `useDebounce()` ✅ - Reusable logic, no global state
- `useLocalStorage()` ✅ - Reusable logic, no global state
- `useWindowSize()` ✅ - Reusable logic, no global state

---

## Summary

### ✅ Final Architecture:

**8 Contexts** (Global State):
1. UserContext - User identification
2. StarredLocationsContext - Starred state
3. ShareContext - Sharing state
4. LocationDataContext - Locations array
5. SelectedLocationContext - Current selection
6. SearchContext - Search state
7. MapInstanceContext - Map instance
8. MapStateContext - Map center/zoom

**Services** (API Calls):
- starService.ts
- shareService.ts
- locationService.ts

**Schemas** (Separate Files):
- api/*.api.schema.ts - API DTOs
- kv/*.kv.schema.ts - KV DTOs
- domain/*.domain.schema.ts - Core entities
- local/*.local.schema.ts - localStorage DTOs

**Components** (UI Only):
- Just consume contexts
- No business logic
- Clean and simple

This is the correct, production-ready architecture!
</result>
</attempt_completion>