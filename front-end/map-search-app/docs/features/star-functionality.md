# Star/Favorite Functionality Design

## Overview
Allow users to "star" or favorite locations and persist this preference. The requirement states: "Save the result to a list and share the list with anyone."

---

## Implementation Approaches

### Approach 1: Client-Side Only (localStorage)
**Best for**: Simple demo, no backend required

```typescript
// Store starred location IDs in localStorage
const STORAGE_KEY = 'starred-locations';

export function getStarredLocationIds(): number[] {
  const stored = localStorage.getItem(STORAGE_KEY);
  return stored ? JSON.parse(stored) : [];
}

export function toggleStar(locationId: number): void {
  const starred = getStarredLocationIds();
  const index = starred.indexOf(locationId);
  
  if (index > -1) {
    starred.splice(index, 1); // Unstar
  } else {
    starred.push(locationId); // Star
  }
  
  localStorage.setItem(STORAGE_KEY, JSON.stringify(starred));
}

export function isStarred(locationId: number): boolean {
  return getStarredLocationIds().includes(locationId);
}

// Generate shareable link
export function getShareableLink(): string {
  const starred = getStarredLocationIds();
  const params = new URLSearchParams({ stars: starred.join(',') });
  return `${window.location.origin}?${params.toString()}`;
}

// Load starred from URL
export function loadStarredFromUrl(): number[] {
  const params = new URLSearchParams(window.location.search);
  const stars = params.get('stars');
  return stars ? stars.split(',').map(Number) : [];
}
```

**Pros:**
- ✅ No backend needed
- ✅ Instant updates
- ✅ Works offline
- ✅ Simple to implement

**Cons:**
- ❌ Only persists in browser
- ❌ Lost if user clears browser data
- ❌ Not synced across devices
- ❌ Sharing requires URL parameters

---

### Approach 2: In-Memory (Session Only)
**Best for**: Quick demo, no persistence needed

```typescript
// In LocationContext
const [starredLocations, setStarredLocations] = useState<Location[]>([]);

const toggleStar = (locationId: number) => {
  setState(prev => {
    const location = prev.locations.find(loc => loc.id === locationId);
    if (!location) return prev;

    const isStarred = prev.starredLocations.some(loc => loc.id === locationId);
    const starredLocations = isStarred
      ? prev.starredLocations.filter(loc => loc.id !== locationId)
      : [...prev.starredLocations, location];

    return { ...prev, starredLocations };
  });
};
```

**Pros:**
- ✅ Simplest implementation
- ✅ No storage needed
- ✅ Fast

**Cons:**
- ❌ Lost on page refresh
- ❌ Can't be shared
- ❌ No persistence

---

### Approach 3: Mock API with In-Memory Storage
**Best for**: Realistic demo with CRUD operations

```typescript
// src/services/mockData.ts
let locations = [...mockLocations];

// Modify location object in place
export async function toggleStarLocation(id: number): Promise<Location> {
  await delay(300);
  
  const location = locations.find(loc => loc.id === id);
  if (!location) {
    throw new Error(`Location with id ${id} not found`);
  }

  // Modify in place (emulates database update)
  location.starred = !location.starred;
  
  return { ...location };
}

// Get all starred locations
export async function fetchStarredLocations(): Promise<Location[]> {
  await delay(200);
  return locations.filter(loc => loc.starred);
}
```

**Pros:**
- ✅ Realistic API behavior
- ✅ Persists during session
- ✅ Can be shared via API
- ✅ Easy to migrate to real API

**Cons:**
- ❌ Lost on server restart
- ❌ Not persistent across sessions
- ❌ Single user only

---

### Approach 4: JSON Server (Persistent Mock API)
**Best for**: Full CRUD demo with persistence

**File: `db.json`**
```json
{
  "locations": [
    {
      "id": 1,
      "name": "Alberts Bike Shop",
      "starred": false,
      ...
    }
  ],
  "starred": [1, 3, 5]
}
```

**Service Implementation:**
```typescript
// Toggle star via API
export async function toggleStarLocation(id: number): Promise<Location> {
  const location = await fetchLocationById(id);
  return updateLocation(id, { starred: !location.starred });
}

// Get starred locations
export async function fetchStarredLocations(): Promise<Location[]> {
  const locations = await fetchLocations();
  return locations.filter(loc => loc.starred);
}
```

**Start JSON Server:**
```bash
npx json-server --watch db.json --port 3001
```

**Pros:**
- ✅ Persistent across sessions
- ✅ Realistic API behavior
- ✅ Full CRUD operations
- ✅ Easy to test

**Cons:**
- ❌ Requires running server
- ❌ File-based (not scalable)
- ❌ Single user only

---

### Approach 5: Hybrid (localStorage + API)
**Best for**: Production-ready with offline support

```typescript
// Sync starred state between localStorage and API
export async function toggleStarLocation(id: number): Promise<Location> {
  // Optimistic update in localStorage
  const starred = getStarredLocationIds();
  const index = starred.indexOf(id);
  
  if (index > -1) {
    starred.splice(index, 1);
  } else {
    starred.push(id);
  }
  
  localStorage.setItem(STORAGE_KEY, JSON.stringify(starred));

  try {
    // Sync with API
    const location = await apiClient.post(`/locations/${id}/star`);
    return location;
  } catch (error) {
    // Rollback on error
    if (index > -1) {
      starred.push(id);
    } else {
      starred.splice(starred.indexOf(id), 1);
    }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(starred));
    throw error;
  }
}
```

**Pros:**
- ✅ Works offline
- ✅ Instant UI updates
- ✅ Syncs with backend
- ✅ Best user experience

**Cons:**
- ❌ More complex
- ❌ Requires sync logic
- ❌ Potential conflicts

---

## Recommended Approach for This Project

### 🎯 Use Approach 3: Mock API with In-Memory Storage

**Why:**
1. **Matches Requirements**: "Data need to be hosted from a mock api server"
2. **Realistic**: Emulates real database behavior
3. **Simple**: Easy to implement and understand
4. **Demonstrable**: Shows CRUD operations
5. **Upgradeable**: Easy to migrate to real API later

### Implementation

**File: `src/services/mockData.ts`**
```typescript
import { Location } from '../types/location.types';

// Convert sample-data.js to TypeScript
// Add starred: false to each location
export const initialLocations: Location[] = [
  {
    id: 1,
    name: 'Alberts Bike Shop',
    location: { lat: 42.354022, lon: -71.046245 },
    details: { ... },
    images: [...],
    starred: false, // Add this field
  },
  // ... rest of locations
];

// In-memory "database" (emulates real database)
let locations = [...initialLocations];
```

**File: `src/services/locationService.ts`**
```typescript
// Modify location object in place (emulates database UPDATE)
export async function toggleStarLocation(id: number): Promise<Location> {
  await delay(300); // Simulate network delay
  
  const location = locations.find(loc => loc.id === id);
  if (!location) {
    throw new Error(`Location with id ${id} not found`);
  }

  // This modifies the object in the array (emulates database update)
  location.starred = !location.starred;
  
  return { ...location }; // Return copy
}

// Fetch only starred locations
export async function fetchStarredLocations(): Promise<Location[]> {
  await delay(200);
  return locations.filter(loc => loc.starred);
}
```

**In LocationContext:**
```typescript
const toggleStar = useCallback(async (locationId: number) => {
  try {
    const updated = await toggleStarLocation(locationId);
    
    // Update local state to reflect change
    setState(prev => ({
      ...prev,
      locations: prev.locations.map(loc =>
        loc.id === locationId ? updated : loc
      ),
      starredLocations: updated.starred
        ? [...prev.starredLocations, updated]
        : prev.starredLocations.filter(loc => loc.id !== locationId),
    }));
  } catch (error) {
    console.error('Failed to toggle star:', error);
  }
}, []);
```

---

## Sharing Starred Locations

### Option 1: URL Parameters (Simple)
```typescript
// Generate shareable link
export function getShareableLink(starredIds: number[]): string {
  const params = new URLSearchParams({
    stars: starredIds.join(',')
  });
  return `${window.location.origin}?${params.toString()}`;
}

// Example: https://yourdomain.com?stars=1,3,5

// Load starred from URL on app init
useEffect(() => {
  const params = new URLSearchParams(window.location.search);
  const starsParam = params.get('stars');
  
  if (starsParam) {
    const starredIds = starsParam.split(',').map(Number);
    // Mark these locations as starred
    starredIds.forEach(id => toggleStar(id));
  }
}, []);
```

### Option 2: Share List API Endpoint (Advanced)
```typescript
// POST /api/share-list
// Creates a shareable list with unique ID

export async function createShareableList(
  locationIds: number[]
): Promise<{ shareId: string; url: string }> {
  const response = await apiClient.post('/share-list', { locationIds });
  return {
    shareId: response.id,
    url: `${window.location.origin}/shared/${response.id}`,
  };
}

// GET /api/share-list/:id
// Retrieves shared list

export async function fetchSharedList(shareId: string): Promise<Location[]> {
  return apiClient.get(`/share-list/${shareId}`);
}

// Example: https://yourdomain.com/shared/abc123
```

---

## UI Components for Star Feature

### Star Button in Modal
```typescript
const StarButton: React.FC<{ location: Location }> = ({ location }) => {
  const { toggleStar } = useLocations();
  const [isStarring, setIsStarring] = useState(false);

  const handleToggle = async () => {
    setIsStarring(true);
    try {
      await toggleStar(location.id);
    } catch (error) {
      console.error('Failed to toggle star:', error);
    } finally {
      setIsStarring(false);
    }
  };

  return (
    <button
      onClick={handleToggle}
      disabled={isStarring}
      className={`star-button ${location.starred ? 'starred' : ''}`}
      aria-label={location.starred ? 'Unstar location' : 'Star location'}
    >
      {location.starred ? '★' : '☆'}
      {location.starred ? 'Starred' : 'Star'}
    </button>
  );
};
```

### Starred Locations List
```typescript
const StarredList: React.FC = () => {
  const { starredLocations } = useLocations();

  if (starredLocations.length === 0) {
    return <p>No starred locations yet</p>;
  }

  return (
    <div className="starred-list">
      <h3>Starred Locations ({starredLocations.length})</h3>
      {starredLocations.map(location => (
        <div key={location.id} className="starred-item">
          <span>{location.name}</span>
          <button onClick={() => viewOnMap(location)}>View</button>
        </div>
      ))}
    </div>
  );
};
```

### Share Button
```typescript
const ShareButton: React.FC = () => {
  const { starredLocations } = useLocations();
  const [shareUrl, setShareUrl] = useState<string>('');

  const handleShare = () => {
    const starredIds = starredLocations.map(loc => loc.id);
    const url = getShareableLink(starredIds);
    setShareUrl(url);
    
    // Copy to clipboard
    navigator.clipboard.writeText(url);
    alert('Share link copied to clipboard!');
  };

  return (
    <button onClick={handleShare} disabled={starredLocations.length === 0}>
      Share Starred Locations ({starredLocations.length})
    </button>
  );
};
```

---

## Data Flow

### Starring a Location:
```
User clicks star button
  ↓
LocationContext.toggleStar(id)
  ↓
locationService.toggleStarLocation(id)
  ↓
Modifies location.starred in mockData array
  ↓
Returns updated location
  ↓
Context updates state
  ↓
UI re-renders with new star status
```

### Sharing Starred Locations:
```
User clicks "Share" button
  ↓
Get all starred location IDs
  ↓
Generate URL with IDs: ?stars=1,3,5
  ↓
Copy to clipboard
  ↓
User shares URL
  ↓
Recipient opens URL
  ↓
App reads ?stars parameter
  ↓
Marks those locations as starred
```

---

## Complete Implementation

### File: `src/services/locationService.ts`

```typescript
import { Location } from '../types/location.types';
import { mockLocations } from './mockData';

// In-memory "database" - emulates real database
let locations = [...mockLocations];

// Simulate network delay
const delay = (ms: number = 300) => new Promise(resolve => setTimeout(resolve, ms));

/**
 * Toggle star status for a location
 * Modifies the location object in place (emulates database UPDATE)
 */
export async function toggleStarLocation(id: number): Promise<Location> {
  await delay(300);
  
  // Find location in our "database"
  const location = locations.find(loc => loc.id === id);
  if (!location) {
    throw new Error(`Location with id ${id} not found`);
  }

  // Modify in place (this is like: UPDATE locations SET starred = !starred WHERE id = ?)
  location.starred = !location.starred;
  
  // Return a copy (API would return updated record)
  return { ...location };
}

/**
 * Fetch all starred locations
 */
export async function fetchStarredLocations(): Promise<Location[]> {
  await delay(200);
  // This is like: SELECT * FROM locations WHERE starred = true
  return locations.filter(loc => loc.starred);
}

/**
 * Star multiple locations (for loading from shared link)
 */
export async function starMultipleLocations(ids: number[]): Promise<Location[]> {
  await delay(300);
  
  const updated: Location[] = [];
  
  for (const id of ids) {
    const location = locations.find(loc => loc.id === id);
    if (location) {
      location.starred = true;
      updated.push({ ...location });
    }
  }
  
  return updated;
}
```

### File: `src/utils/shareUtils.ts`

```typescript
/**
 * Generate a shareable URL with starred location IDs
 */
export function generateShareUrl(starredLocationIds: number[]): string {
  if (starredLocationIds.length === 0) {
    return window.location.origin;
  }

  const params = new URLSearchParams({
    stars: starredLocationIds.join(','),
  });

  return `${window.location.origin}?${params.toString()}`;
}

/**
 * Parse starred location IDs from URL
 */
export function parseStarredFromUrl(): number[] {
  const params = new URLSearchParams(window.location.search);
  const starsParam = params.get('stars');
  
  if (!starsParam) return [];
  
  return starsParam
    .split(',')
    .map(Number)
    .filter(id => !isNaN(id));
}

/**
 * Copy text to clipboard
 */
export async function copyToClipboard(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (error) {
    console.error('Failed to copy to clipboard:', error);
    return false;
  }
}
```

### File: `src/contexts/LocationContext.tsx` (Updated)

```typescript
export const LocationProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, setState] = useState<LocationState>({
    locations: [],
    selectedLocation: null,
    starredLocations: [],
  });

  // Load initial data
  useEffect(() => {
    const loadData = async () => {
      const locations = await fetchLocations();
      
      // Check URL for shared starred locations
      const sharedStarredIds = parseStarredFromUrl();
      if (sharedStarredIds.length > 0) {
        await starMultipleLocations(sharedStarredIds);
        // Reload to get updated starred status
        const updated = await fetchLocations();
        setState(prev => ({
          ...prev,
          locations: updated,
          starredLocations: updated.filter(loc => loc.starred),
        }));
      } else {
        setState(prev => ({
          ...prev,
          locations,
          starredLocations: locations.filter(loc => loc.starred),
        }));
      }
    };

    loadData();
  }, []);

  const toggleStar = useCallback(async (locationId: number) => {
    try {
      const updated = await toggleStarLocation(locationId);
      
      setState(prev => ({
        ...prev,
        locations: prev.locations.map(loc =>
          loc.id === locationId ? updated : loc
        ),
        starredLocations: updated.starred
          ? [...prev.starredLocations, updated]
          : prev.starredLocations.filter(loc => loc.id !== locationId),
      }));
    } catch (error) {
      console.error('Failed to toggle star:', error);
    }
  }, []);

  // ... rest of context
};
```

---

## Summary

### ✅ Recommended: Approach 3 (Mock API with In-Memory)

**Yes, we modify the sample data object in place to emulate a database.**

This approach:
- ✅ Emulates real database UPDATE operations
- ✅ Persists during development session
- ✅ Demonstrates CRUD operations
- ✅ Easy to understand and test
- ✅ Realistic API behavior
- ✅ Can be shared via URL parameters

### How It Works:

1. **Initial Load**: Copy `mockLocations` to `locations` array
2. **Toggle Star**: Find location in array, flip `starred` boolean
3. **Fetch Starred**: Filter array where `starred === true`
4. **Share**: Generate URL with starred IDs: `?stars=1,3,5`
5. **Load Shared**: Parse URL, mark those locations as starred

### Migration Path:

**Development** → **JSON Server** → **Real API**

The service interface stays the same, just swap the implementation!

---

## File Location

**[`front-end/map-search-app/docs/features/star-functionality.md`](front-end/map-search-app/docs/features/star-functionality.md)**

This document covers all approaches with complete code examples for the star/favorite functionality.
</result>
</attempt_completion>