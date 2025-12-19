# Location Service with Cloudflare KV + localStorage

## Overview
A hybrid approach using localStorage for client-side operations and Cloudflare KV for sharing functionality. Provides the best of both worlds: instant local updates and shareable lists.

---

## Architecture

### Two-Tier Storage:

```
┌─────────────────────────────────────┐
│ Client-Side (localStorage)          │
│                                     │
│ - All locations                     │
│ - Starred status                    │
│ - CRUD operations                   │
│ - Instant updates                   │
└─────────────────────────────────────┘
              ↕️ (Only for sharing)
┌─────────────────────────────────────┐
│ Server-Side (Cloudflare KV)         │
│                                     │
│ - Shared lists only                 │
│ - { "abc123": [1, 3, 5] }          │
│ - 30-day expiration                 │
│ - Global edge network               │
└─────────────────────────────────────┘
```

---

## Client-Side: localStorage (Primary Storage)

### File: `src/services/localStorage.ts`

```typescript
const STORAGE_KEYS = {
  LOCATIONS: 'map-search-locations',
  NEXT_ID: 'map-search-next-id',
};

export function getItem<T>(key: string, defaultValue: T): T {
  try {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : defaultValue;
  } catch (error) {
    console.error(`Error reading from localStorage:`, error);
    return defaultValue;
  }
}

export function setItem<T>(key: string, value: T): void {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch (error) {
    console.error(`Error writing to localStorage:`, error);
  }
}
```

### File: `src/services/locationService.ts`

```typescript
import { Location } from '../types/location.types';
import { initialLocations } from './mockData';
import { getItem, setItem } from './localStorage';

const STORAGE_KEYS = {
  LOCATIONS: 'map-search-locations',
  NEXT_ID: 'map-search-next-id',
};

// Initialize localStorage with seed data
function initializeStorage(): void {
  const existing = getItem<Location[]>(STORAGE_KEYS.LOCATIONS, []);
  if (existing.length === 0) {
    setItem(STORAGE_KEYS.LOCATIONS, initialLocations);
    setItem(STORAGE_KEYS.NEXT_ID, 16);
  }
}

initializeStorage();

function getLocations(): Location[] {
  return getItem<Location[]>(STORAGE_KEYS.LOCATIONS, []);
}

function saveLocations(locations: Location[]): void {
  setItem(STORAGE_KEYS.LOCATIONS, locations);
}

// Simulate network delay for realistic UX
const delay = (ms: number = 200) => new Promise(resolve => setTimeout(resolve, ms));

/**
 * Fetch all locations from localStorage
 */
export async function fetchLocations(): Promise<Location[]> {
  await delay(200);
  return getLocations();
}

/**
 * Fetch single location by ID
 */
export async function fetchLocationById(id: number): Promise<Location> {
  await delay(150);
  const locations = getLocations();
  const location = locations.find(loc => loc.id === id);
  if (!location) throw new Error(`Location ${id} not found`);
  return location;
}

/**
 * Search locations by query
 */
export async function searchLocations(query: string): Promise<Location[]> {
  await delay(200);
  const locations = getLocations();
  const lowerQuery = query.toLowerCase().trim();
  if (!lowerQuery) return [];

  return locations.filter(location =>
    location.name.toLowerCase().includes(lowerQuery) ||
    location.details?.description?.toLowerCase().includes(lowerQuery)
  );
}

/**
 * Create new location
 */
export async function createLocation(locationData: Omit<Location, 'id'>): Promise<Location> {
  await delay(300);
  const locations = getLocations();
  const nextId = getItem<number>(STORAGE_KEYS.NEXT_ID, 16);
  
  const newLocation: Location = {
    ...locationData,
    id: nextId,
    starred: false,
  };

  locations.push(newLocation);
  saveLocations(locations);
  setItem(STORAGE_KEYS.NEXT_ID, nextId + 1);
  
  return newLocation;
}

/**
 * Update existing location
 */
export async function updateLocation(
  id: number,
  updates: Partial<Location>
): Promise<Location> {
  await delay(300);
  const locations = getLocations();
  const index = locations.findIndex(loc => loc.id === id);
  if (index === -1) throw new Error(`Location ${id} not found`);

  locations[index] = { ...locations[index], ...updates };
  saveLocations(locations);
  return locations[index];
}

/**
 * Delete location
 */
export async function deleteLocation(id: number): Promise<void> {
  await delay(300);
  const locations = getLocations();
  const filtered = locations.filter(loc => loc.id !== id);
  if (filtered.length === locations.length) {
    throw new Error(`Location ${id} not found`);
  }
  saveLocations(filtered);
}

/**
 * Toggle star status
 */
export async function toggleStarLocation(id: number): Promise<Location> {
  await delay(200);
  const locations = getLocations();
  const location = locations.find(loc => loc.id === id);
  if (!location) throw new Error(`Location ${id} not found`);

  location.starred = !location.starred;
  saveLocations(locations);
  return { ...location };
}

/**
 * Fetch all starred locations
 */
export async function fetchStarredLocations(): Promise<Location[]> {
  await delay(150);
  return getLocations().filter(loc => loc.starred);
}

/**
 * Star multiple locations (for loading shared lists)
 */
export async function starMultipleLocations(ids: number[]): Promise<Location[]> {
  await delay(300);
  const locations = getLocations();
  const updated: Location[] = [];

  for (const id of ids) {
    const location = locations.find(loc => loc.id === id);
    if (location) {
      location.starred = true;
      updated.push({ ...location });
    }
  }

  saveLocations(locations);
  return updated;
}
```

---

## Server-Side: Cloudflare KV (Sharing Only)

### Cloudflare Worker for Sharing

**File: `workers/share-api/src/index.ts`**

```typescript
export interface Env {
  SHARED_LISTS: KVNamespace;
}

interface SharedList {
  locationIds: number[];
  createdAt: number;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // POST /api/share - Create shared list
    if (url.pathname === '/api/share' && request.method === 'POST') {
      try {
        const { locationIds } = await request.json<{ locationIds: number[] }>();
        
        if (!Array.isArray(locationIds) || locationIds.length === 0) {
          return new Response('Invalid locationIds', { status: 400, headers: corsHeaders });
        }

        // Generate unique 8-character ID
        const shareId = crypto.randomUUID().slice(0, 8);
        
        const sharedList: SharedList = {
          locationIds,
          createdAt: Date.now(),
        };

        // Store in KV with 30-day expiration
        await env.SHARED_LISTS.put(
          shareId,
          JSON.stringify(sharedList),
          { expirationTtl: 60 * 60 * 24 * 30 } // 30 days
        );

        return new Response(
          JSON.stringify({
            shareId,
            url: `${url.origin}/shared/${shareId}`,
            expiresAt: Date.now() + (60 * 60 * 24 * 30 * 1000),
          }),
          { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
        );
      } catch (error) {
        return new Response('Internal Server Error', { status: 500, headers: corsHeaders });
      }
    }

    // GET /api/share/:id - Retrieve shared list
    if (url.pathname.startsWith('/api/share/') && request.method === 'GET') {
      const shareId = url.pathname.split('/').pop();
      
      if (!shareId) {
        return new Response('Invalid share ID', { status: 400, headers: corsHeaders });
      }

      const data = await env.SHARED_LISTS.get(shareId);
      
      if (!data) {
        return new Response(
          JSON.stringify({ error: 'Shared list not found or expired' }),
          { status: 404, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
        );
      }

      return new Response(data, {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    return new Response('Not Found', { status: 404, headers: corsHeaders });
  },
};
```

---

## Client-Side: Share Service

### File: `src/services/shareService.ts`

```typescript
const API_URL = import.meta.env.VITE_SHARE_API_URL || '/api';

export interface ShareResult {
  shareId: string;
  url: string;
  expiresAt: number;
}

/**
 * Create a shareable list using Cloudflare KV
 */
export async function createSharedList(locationIds: number[]): Promise<ShareResult> {
  const response = await fetch(`${API_URL}/share`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ locationIds }),
  });

  if (!response.ok) {
    throw new Error('Failed to create shared list');
  }

  return response.json();
}

/**
 * Retrieve a shared list from Cloudflare KV
 */
export async function getSharedList(shareId: string): Promise<number[]> {
  const response = await fetch(`${API_URL}/share/${shareId}`);

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Shared list not found or expired');
    }
    throw new Error('Failed to fetch shared list');
  }

  const data = await response.json();
  return data.locationIds;
}

/**
 * Copy share URL to clipboard
 */
export async function copyShareUrl(url: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(url);
    return true;
  } catch (error) {
    console.error('Failed to copy to clipboard:', error);
    return false;
  }
}
```

---

## React Integration

### ShareButton Component

**File: `src/components/Share/ShareButton.tsx`**

```typescript
import React, { useState, useCallback } from 'react';
import { useStarredLocations } from '@contexts/StarredLocationsContext';
import { createSharedList, copyShareUrl } from '@services/shareService';

const ShareButton: React.FC = () => {
  const { starredLocationIds } = useStarredLocations();
  const [shareUrl, setShareUrl] = useState<string>('');
  const [isSharing, setIsSharing] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleShare = useCallback(async () => {
    if (starredLocationIds.length === 0) return;

    setIsSharing(true);
    try {
      // Create shared list in Cloudflare KV
      const result = await createSharedList(starredLocationIds);
      setShareUrl(result.url);
      
      // Copy to clipboard
      const success = await copyShareUrl(result.url);
      if (success) {
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      }
    } catch (error) {
      console.error('Failed to create share link:', error);
      alert('Failed to create share link. Please try again.');
    } finally {
      setIsSharing(false);
    }
  }, [starredLocationIds]);

  if (starredLocationIds.length === 0) {
    return null;
  }

  return (
    <div className="share-container">
      <button
        onClick={handleShare}
        disabled={isSharing}
        className="share-button"
      >
        {isSharing ? 'Creating link...' : `Share ${starredLocationIds.length} Starred`}
      </button>
      
      {copied && (
        <span className="share-success">✓ Link copied to clipboard!</span>
      )}
      
      {shareUrl && (
        <div className="share-url">
          <input
            type="text"
            value={shareUrl}
            readOnly
            onClick={(e) => e.currentTarget.select()}
          />
        </div>
      )}
    </div>
  );
};

export default ShareButton;
```

### Load Shared List on App Mount

**File: `src/App.tsx`** (add to existing)

```typescript
import { useEffect } from 'react';
import { useStarredLocations } from '@contexts/StarredLocationsContext';
import { getSharedList } from '@services/shareService';
import { starMultipleLocations } from '@services/locationService';

const App: React.FC = () => {
  const { refreshStarred } = useStarredLocations();

  // Load shared list if URL matches /shared/:id
  useEffect(() => {
    const loadSharedList = async () => {
      const path = window.location.pathname;
      const match = path.match(/^\/shared\/([a-z0-9]+)$/);
      
      if (match) {
        const shareId = match[1];
        try {
          // Fetch shared list from Cloudflare KV
          const locationIds = await getSharedList(shareId);
          
          // Star those locations in localStorage
          await starMultipleLocations(locationIds);
          
          // Refresh starred context
          refreshStarred();
          
          // Optional: Show success message
          console.log(`Loaded ${locationIds.length} shared locations`);
        } catch (error) {
          console.error('Failed to load shared list:', error);
          alert('This shared link is invalid or has expired.');
        }
      }
    };

    loadSharedList();
  }, [refreshStarred]);

  // ... rest of App component
};
```

---

## Cloudflare Worker Setup

### Step 1: Create Worker Project

```bash
cd front-end
mkdir -p workers/share-api
cd workers/share-api

# Initialize Worker
wrangler init

# Select:
# - TypeScript: Yes
# - Fetch handler: Yes
# - Deploy: No (we'll do it manually)
```

### Step 2: Create KV Namespace

```bash
# Create KV namespace
wrangler kv:namespace create SHARED_LISTS

# Output will show:
# [[kv_namespaces]]
# binding = "SHARED_LISTS"
# id = "abc123def456..."

# Copy the ID for next step
```

### Step 3: Configure wrangler.toml

**File: `workers/share-api/wrangler.toml`**

```toml
name = "share-api"
main = "src/index.ts"
compatibility_date = "2024-01-01"

# Add KV namespace binding
[[kv_namespaces]]
binding = "SHARED_LISTS"
id = "your-kv-namespace-id-here"

# Production environment
[env.production]
name = "share-api-production"
[[env.production.kv_namespaces]]
binding = "SHARED_LISTS"
id = "your-production-kv-id-here"
```

### Step 4: Deploy Worker

```bash
# Deploy to Cloudflare
wrangler deploy

# Output:
# Published share-api
# https://share-api.your-subdomain.workers.dev
```

### Step 5: Update Client Environment

**File: `front-end/map-search-app/.env`**

```env
# Add Worker URL
VITE_SHARE_API_URL=https://share-api.your-subdomain.workers.dev/api
```

---

## Routing Setup

### Option 1: Client-Side Routing (React Router)

```bash
npm install react-router-dom
```

**File: `src/main.tsx`**

```typescript
import { BrowserRouter, Routes, Route } from 'react-router-dom';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <LocationDataProvider>
        {/* ... other providers */}
        <Routes>
          <Route path="/" element={<App />} />
          <Route path="/shared/:shareId" element={<App />} />
        </Routes>
      </LocationDataProvider>
    </BrowserRouter>
  </React.StrictMode>
);
```

### Option 2: Simple Path Matching (No Router)

```typescript
// In App.tsx
useEffect(() => {
  const path = window.location.pathname;
  
  // Match /shared/:id
  if (path.startsWith('/shared/')) {
    const shareId = path.split('/')[2];
    loadSharedList(shareId);
  }
}, []);
```

---

## Data Flow

### Creating a Share:

```
1. User stars locations (stored in localStorage)
2. User clicks "Share" button
3. Client sends starred IDs to Worker: POST /api/share { locationIds: [1,3,5] }
4. Worker generates unique ID: "abc123"
5. Worker stores in KV: { "abc123": { locationIds: [1,3,5], createdAt: ... } }
6. Worker returns: { shareId: "abc123", url: "https://yourdomain.com/shared/abc123" }
7. Client copies URL to clipboard
8. User shares URL
```

### Loading a Share:

```
1. Friend opens: https://yourdomain.com/shared/abc123
2. App detects /shared/:id route
3. Client fetches from Worker: GET /api/share/abc123
4. Worker retrieves from KV: { locationIds: [1,3,5], createdAt: ... }
5. Worker returns location IDs
6. Client marks those locations as starred in localStorage
7. Friend sees the shared starred locations!
```

---

## Benefits of This Hybrid Approach

### ✅ Best of Both Worlds:

1. **localStorage for Primary Storage:**
   - ✅ Instant CRUD operations
   - ✅ Works offline
   - ✅ No API calls for normal usage
   - ✅ Persists across sessions

2. **Cloudflare KV for Sharing:**
   - ✅ Clean URLs (`/shared/abc123`)
   - ✅ Global distribution
   - ✅ Fast (<50ms)
   - ✅ Free tier sufficient
   - ✅ 30-day expiration

### Performance:

- **Normal usage**: 0ms (localStorage)
- **Create share**: ~100ms (KV write)
- **Load share**: ~50ms (KV read from edge)

### Cost:

- **localStorage**: Free, unlimited
- **Cloudflare KV**: Free (within generous limits)
- **Total**: $0

---

## Alternative: Cloudflare Pages Functions

### Even Simpler: No Separate Worker Needed!

Cloudflare Pages supports Functions (serverless functions in your Pages project).

**File: `functions/api/share.ts`** (in Pages project)

```typescript
interface Env {
  SHARED_LISTS: KVNamespace;
}

export const onRequestPost: PagesFunction<Env> = async (context) => {
  const { locationIds } = await context.request.json();
  const shareId = crypto.randomUUID().slice(0, 8);
  
  await context.env.SHARED_LISTS.put(
    shareId,
    JSON.stringify({ locationIds, createdAt: Date.now() }),
    { expirationTtl: 60 * 60 * 24 * 30 }
  );

  return new Response(JSON.stringify({
    shareId,
    url: `${new URL(context.request.url).origin}/shared/${shareId}`,
  }));
};

export const onRequestGet: PagesFunction<Env> = async (context) => {
  const shareId = context.params.id as string;
  const data = await context.env.SHARED_LISTS.get(shareId);
  
  if (!data) {
    return new Response('Not found', { status: 404 });
  }

  return new Response(data, {
    headers: { 'Content-Type': 'application/json' },
  });
};
```

**File structure:**
```
front-end/map-search-app/
├── functions/
│   └── api/
│       ├── share.ts           # POST /api/share
│       └── share/
│           └── [id].ts        # GET /api/share/:id
├── src/
└── public/
```

**Benefits:**
- ✅ No separate Worker deployment
- ✅ Same domain (no CORS issues)
- ✅ Deployed automatically with Pages
- ✅ Even simpler setup

---

## Setup Instructions

### Using Pages Functions (Recommended):

```bash
# 1. Create KV namespace
wrangler kv:namespace create SHARED_LISTS

# 2. Add to Pages project settings
# Go to Cloudflare Dashboard → Pages → Your Project → Settings → Functions
# Add KV binding: SHARED_LISTS → your-kv-id

# 3. Create functions/ directory in project
mkdir -p functions/api/share

# 4. Add function files (see above)

# 5. Deploy
git push origin main
# Cloudflare Pages automatically deploys with Functions!
```

**That's it!** No separate Worker needed.

---

## Environment Variables

**File: `front-end/map-search-app/.env`**

```env
# Google Maps
VITE_GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here

# Share API (same domain when using Pages Functions)
VITE_SHARE_API_URL=/api

# Server config
VITE_SERVER_HOST=137.184.37.88
VITE_SERVER_PORT=5173
VITE_BASE_URL=http://137.184.37.88:5173
```

---

## Summary

### ✅ Recommended: Cloudflare KV with Pages Functions

**Why:**
1. **Same platform** - No separate Worker
2. **Same domain** - No CORS issues
3. **Auto-deploy** - Deploys with Pages
4. **Free** - Generous limits
5. **Fast** - Edge network
6. **Simple** - Just add `functions/` directory

### Implementation:

**Primary Storage**: localStorage (instant, offline)
**Sharing**: Cloudflare KV via Pages Functions (clean URLs, global)

**Setup time**: ~30 minutes
**Cost**: $0
**Complexity**: Low

This is the perfect solution for your map search project!