# Location Service with localStorage Implementation

## Overview
A client-side service that uses localStorage to persist location data and modifications. Provides full CRUD operations with data persistence across browser sessions.

---

## Architecture

### Data Storage Strategy
```typescript
// localStorage keys
const STORAGE_KEYS = {
  LOCATIONS: 'map-search-locations',
  STARRED: 'map-search-starred-ids',
  NEXT_ID: 'map-search-next-id',
};

// Data is stored as JSON in localStorage
localStorage.setItem(STORAGE_KEYS.LOCATIONS, JSON.stringify(locations));
```

### Benefits of localStorage:
- ✅ Persists across browser sessions
- ✅ No backend required
- ✅ Instant updates (no network delay)
- ✅ Works offline
- ✅ Easy to implement
- ✅ Can still be "shared" via URL parameters

---

## Complete Implementation

### File: `src/services/localStorage.ts`

```typescript
/**
 * localStorage utility functions with type safety
 */

export function getItem<T>(key: string, defaultValue: T): T {
  try {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : defaultValue;
  } catch (error) {
    console.error(`Error reading from localStorage key "${key}":`, error);
    return defaultValue;
  }
}

export function setItem<T>(key: string, value: T): void {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch (error) {
    console.error(`Error writing to localStorage key "${key}":`, error);
  }
}

export function removeItem(key: string): void {
  try {
    localStorage.removeItem(key);
  } catch (error) {
    console.error(`Error removing localStorage key "${key}":`, error);
  }
}

export function clear(): void {
  try {
    localStorage.clear();
  } catch (error) {
    console.error('Error clearing localStorage:', error);
  }
}
```

### File: `src/services/mockData.ts`

```typescript
import { Location } from '../types/location.types';

// Initial seed data from sample-data.js
export const initialLocations: Location[] = [
  {
    id: 1,
    name: 'Alberts Bike Shop',
    location: {
      lat: 42.354022,
      lon: -71.046245,
    },
    details: {
      description: 'We buy and sell used bikes and equipment. Contact us today to get moving!',
      website: 'https://groundsignal.com',
    },
    images: [
      'http://dspncdn.com/a1/media/692x/f8/58/77/f85877c41fb6147599886048e3582d47.jpg',
      'https://s-media-cache-ak0.pinimg.com/236x/96/f0/c4/96f0c45570b80b7024d3d549509fde4e.jpg',
      'http://68.media.tumblr.com/f62950453d60c9a873b35d7f2fcf4ace/tumblr_mjd4b4nD0q1qakvm6o1_1280.jpg',
    ],
    starred: false,
  },
  {
    id: 2,
    name: 'Arctic Ice Cream',
    location: {
      lat: 42.364369,
      lon: -71.063776,
    },
    details: {
      description: "We sell the coldest ice cream you've ever had! It's freezing cold. Literally.",
      website: 'https://groundsignal.com',
      avgStoreTraffic: {
        monday: null,
        tuesday: 504,
        wednesday: 607,
        thursday: 705,
        friday: 714,
        saturday: 1918,
        sunday: 1295,
      },
    },
    images: [
      'https://s.yimg.com/ny/api/res/1.2/Lqp5sa6BMjWgIpAZGJ9apQ--/YXBwaWQ9aGlnaGxhbmRlcjtzbT0xO3c9Mzc4O2g9Mzc4/http://media.zenfs.com/en-US/homerun/spoon_university_184/90c834e4ac8b84e06606743451310bea',
      'https://s3.burpple.com/foods/c9a13bb614df68a09a381856_original.?1363868049',
      'https://s-media-cache-ak0.pinimg.com/736x/88/6c/cd/886ccd8e288e4a83130c7c44582eb618.jpg',
    ],
    starred: false,
  },
  {
    id: 3,
    name: 'Clems Carwash',
    location: {
      lat: 42.367793,
      lon: -71.081200,
    },
    details: {
      description: 'The nations largest provider of car washes since 1907. Come in and enjoy a car wash that will literally peel the rust right off!',
      website: 'https://groundsignal.com',
    },
    images: [
      'https://rainbowgram.files.wordpress.com/2015/03/fe8de-10787805_946218992085237_543029709_n.jpg?w=640',
      'https://scontent.cdninstagram.com/hphotos-xfa1/t51.2885-15/s640x640/e35/sh0.08/11255060_1622514958029454_1290485308_n.jpg',
    ],
    starred: false,
  },
  {
    id: 4,
    name: 'Pets Plus',
    location: {
      lat: 42.331319,
      lon: -71.044207,
    },
    details: {
      description: "We sell pets PLUS almost everything else. Seriously. We're also the largest owner of albino dwarf hamsters in North America.",
      avgStoreTraffic: {
        monday: 12,
        tuesday: 37,
        wednesday: 117,
        thursday: 197,
        friday: 105,
        saturday: 98,
        sunday: 45,
      },
    },
    images: [
      'https://scontent.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/17438950_343266982735997_4166148432085385216_n.jpg',
    ],
    starred: false,
  },
  {
    id: 5,
    name: 'Evans Bakery',
    location: {
      lat: 42.373056,
      lon: -70.993910,
    },
    details: {
      description: "Evan has been baking bread since he was 6 months old. Known around the world for his homemade english muffins, he's been featured in Healthy Living an incredible 118 times. Come in to experience the magic of homemade bread!",
    },
    images: [
      'https://s-media-cache-ak0.pinimg.com/736x/4c/0a/c1/4c0ac1e45df77367c680ce4bbf9e1ffc.jpg',
      'http://68.media.tumblr.com/7f8a8514a88c893bac6c6db9b4093627/tumblr_n8j8uuygEf1r1thfzo5_1280.jpg',
      'https://s-media-cache-ak0.pinimg.com/736x/eb/73/09/eb7309d64f419eb7f714ef64dcb65287--sourdough-bread-bread-recipes.jpg',
    ],
    starred: false,
  },
  {
    id: 6,
    name: 'The Secret Store',
    location: {
      lat: 42.344516,
      lon: -70.953655,
    },
    starred: false,
  },
  {
    id: 7,
    name: 'Shoes on Shoes',
    location: {
      lat: 42.365066,
      lon: -71.019402,
    },
    starred: false,
  },
  {
    id: 8,
    name: 'Bertas Bees',
    location: {
      lat: 42.368554,
      lon: -71.038971,
    },
    starred: false,
  },
  {
    id: 9,
    name: 'The Cranky Elf',
    location: {
      lat: 42.375720,
      lon: -71.056395,
    },
    starred: false,
  },
  {
    id: 10,
    name: 'Nanas Bananas',
    location: {
      lat: 42.362593,
      lon: -71.082315,
    },
    starred: false,
  },
  {
    id: 11,
    name: 'Cycling for Cyclists',
    location: {
      lat: 42.360129,
      lon: -71.094160,
    },
    starred: false,
  },
  {
    id: 12,
    name: 'The Ugly Kitten',
    location: {
      lat: 42.350669,
      lon: -71.089354,
    },
    starred: false,
  },
  {
    id: 13,
    name: 'Family Boots',
    location: {
      lat: 42.350732,
      lon: -71.080427,
    },
    starred: false,
  },
  {
    id: 14,
    name: "Smoothies 'n Things",
    location: {
      lat: 42.344204,
      lon: -71.077423,
    },
    starred: false,
  },
  {
    id: 15,
    name: 'Johnys Furniture',
    location: {
      lat: 42.342332,
      lon: -71.075191,
    },
    starred: false,
  },
];
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

// Simulate network delay for realistic UX
const delay = (ms: number = 300) => new Promise(resolve => setTimeout(resolve, ms));

/**
 * Initialize localStorage with seed data if empty
 */
function initializeStorage(): void {
  const existing = getItem<Location[]>(STORAGE_KEYS.LOCATIONS, []);
  
  if (existing.length === 0) {
    setItem(STORAGE_KEYS.LOCATIONS, initialLocations);
    const maxId = Math.max(...initialLocations.map(l => l.id));
    setItem(STORAGE_KEYS.NEXT_ID, maxId + 1);
  }
}

// Initialize on module load
initializeStorage();

/**
 * Get all locations from localStorage
 */
function getLocations(): Location[] {
  return getItem<Location[]>(STORAGE_KEYS.LOCATIONS, []);
}

/**
 * Save locations to localStorage
 */
function saveLocations(locations: Location[]): void {
  setItem(STORAGE_KEYS.LOCATIONS, locations);
}

/**
 * Get next available ID
 */
function getNextId(): number {
  const nextId = getItem<number>(STORAGE_KEYS.NEXT_ID, 16);
  setItem(STORAGE_KEYS.NEXT_ID, nextId + 1);
  return nextId;
}

/**
 * Fetch all locations
 */
export async function fetchLocations(): Promise<Location[]> {
  await delay(200);
  return getLocations();
}

/**
 * Fetch a single location by ID
 */
export async function fetchLocationById(id: number): Promise<Location> {
  await delay(150);
  
  const locations = getLocations();
  const location = locations.find(loc => loc.id === id);
  
  if (!location) {
    throw new Error(`Location with id ${id} not found`);
  }
  
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
 * Create a new location
 */
export async function createLocation(
  locationData: Omit<Location, 'id'>
): Promise<Location> {
  await delay(300);
  
  const locations = getLocations();
  const newLocation: Location = {
    ...locationData,
    id: getNextId(),
    starred: false,
  };

  locations.push(newLocation);
  saveLocations(locations);
  
  return newLocation;
}

/**
 * Update an existing location
 */
export async function updateLocation(
  id: number,
  updates: Partial<Location>
): Promise<Location> {
  await delay(300);
  
  const locations = getLocations();
  const index = locations.findIndex(loc => loc.id === id);
  
  if (index === -1) {
    throw new Error(`Location with id ${id} not found`);
  }

  locations[index] = { ...locations[index], ...updates };
  saveLocations(locations);
  
  return locations[index];
}

/**
 * Delete a location
 */
export async function deleteLocation(id: number): Promise<void> {
  await delay(300);
  
  const locations = getLocations();
  const filtered = locations.filter(loc => loc.id !== id);
  
  if (filtered.length === locations.length) {
    throw new Error(`Location with id ${id} not found`);
  }

  saveLocations(filtered);
}

/**
 * Toggle star status for a location
 */
export async function toggleStarLocation(id: number): Promise<Location> {
  await delay(200);
  
  const locations = getLocations();
  const location = locations.find(loc => loc.id === id);
  
  if (!location) {
    throw new Error(`Location with id ${id} not found`);
  }

  // Toggle starred status
  location.starred = !location.starred;
  saveLocations(locations);
  
  return { ...location };
}

/**
 * Fetch all starred locations
 */
export async function fetchStarredLocations(): Promise<Location[]> {
  await delay(150);
  
  const locations = getLocations();
  return locations.filter(loc => loc.starred);
}

/**
 * Star multiple locations (for loading from shared link)
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

/**
 * Reset to initial data (useful for development/testing)
 */
export async function resetToInitialData(): Promise<Location[]> {
  await delay(200);
  
  setItem(STORAGE_KEYS.LOCATIONS, initialLocations);
  const maxId = Math.max(...initialLocations.map(l => l.id));
  setItem(STORAGE_KEYS.NEXT_ID, maxId + 1);
  
  return initialLocations;
}

/**
 * Export all data (for backup/sharing)
 */
export function exportData(): string {
  const locations = getLocations();
  return JSON.stringify(locations, null, 2);
}

/**
 * Import data (from backup/sharing)
 */
export async function importData(jsonData: string): Promise<Location[]> {
  await delay(300);
  
  try {
    const locations = JSON.parse(jsonData) as Location[];
    saveLocations(locations);
    return locations;
  } catch (error) {
    throw new Error('Invalid JSON data');
  }
}
```

---

## Sharing Functionality

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
 * Copy share URL to clipboard
 */
export async function copyShareUrl(starredLocationIds: number[]): Promise<boolean> {
  const url = generateShareUrl(starredLocationIds);
  
  try {
    await navigator.clipboard.writeText(url);
    return true;
  } catch (error) {
    console.error('Failed to copy to clipboard:', error);
    
    // Fallback: create temporary input
    const input = document.createElement('input');
    input.value = url;
    document.body.appendChild(input);
    input.select();
    const success = document.execCommand('copy');
    document.body.removeChild(input);
    
    return success;
  }
}

/**
 * Share via Web Share API (mobile)
 */
export async function shareViaWebShare(
  starredLocationIds: number[],
  locationNames: string[]
): Promise<boolean> {
  if (!navigator.share) {
    return false; // Web Share API not supported
  }

  const url = generateShareUrl(starredLocationIds);
  
  try {
    await navigator.share({
      title: 'My Starred Locations',
      text: `Check out these ${starredLocationIds.length} locations: ${locationNames.join(', ')}`,
      url,
    });
    return true;
  } catch (error) {
    if (error instanceof Error && error.name === 'AbortError') {
      // User cancelled share
      return false;
    }
    console.error('Failed to share:', error);
    return false;
  }
}
```

---

## Context Integration

### File: `src/contexts/LocationContext.tsx` (Updated)

```typescript
import React, { createContext, useContext, useState, useCallback, useEffect, ReactNode } from 'react';
import { Location, LocationContextType, LocationState } from '../types/location.types';
import * as locationService from '../services/locationService';
import { parseStarredFromUrl } from '../utils/shareUtils';

const LocationContext = createContext<LocationContextType | undefined>(undefined);

export const LocationProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, setState] = useState<LocationState>({
    locations: [],
    selectedLocation: null,
    starredLocations: [],
  });

  // Load initial data from localStorage
  useEffect(() => {
    const loadData = async () => {
      try {
        const locations = await locationService.fetchLocations();
        
        // Check URL for shared starred locations
        const sharedStarredIds = parseStarredFromUrl();
        if (sharedStarredIds.length > 0) {
          // Star the shared locations
          await locationService.starMultipleLocations(sharedStarredIds);
          // Reload to get updated data
          const updated = await locationService.fetchLocations();
          setState({
            locations: updated,
            selectedLocation: null,
            starredLocations: updated.filter(loc => loc.starred),
          });
        } else {
          setState({
            locations,
            selectedLocation: null,
            starredLocations: locations.filter(loc => loc.starred),
          });
        }
      } catch (error) {
        console.error('Failed to load locations:', error);
      }
    };

    loadData();
  }, []);

  const toggleStar = useCallback(async (locationId: number) => {
    try {
      const updated = await locationService.toggleStarLocation(locationId);
      
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
      throw error;
    }
  }, []);

  // ... rest of context methods

  const value: LocationContextType = {
    ...state,
    setSelectedLocation,
    toggleStar,
    addLocation,
    updateLocation,
    deleteLocation,
  };

  return <LocationContext.Provider value={value}>{children}</LocationContext.Provider>;
};

export const useLocations = (): LocationContextType => {
  const context = useContext(LocationContext);
  if (!context) {
    throw new Error('useLocations must be used within LocationProvider');
  }
  return context;
};
```

---

## UI Components

### Share Button Component

```typescript
import React, { useState } from 'react';
import { useLocations } from '@contexts/LocationContext';
import { copyShareUrl } from '@utils/shareUtils';

const ShareButton: React.FC = () => {
  const { starredLocations } = useLocations();
  const [copied, setCopied] = useState(false);

  const handleShare = async () => {
    const starredIds = starredLocations.map(loc => loc.id);
    const success = await copyShareUrl(starredIds);
    
    if (success) {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  if (starredLocations.length === 0) {
    return null; // Don't show if no starred locations
  }

  return (
    <button
      onClick={handleShare}
      className="share-button"
      title="Share your starred locations"
    >
      {copied ? '✓ Copied!' : `Share ${starredLocations.length} Starred`}
    </button>
  );
};

export default ShareButton;
```

### Star Toggle Button

```typescript
import React from 'react';
import { useLocations } from '@contexts/LocationContext';

interface StarButtonProps {
  locationId: number;
  className?: string;
}

const StarButton: React.FC<StarButtonProps> = ({ locationId, className }) => {
  const { locations, toggleStar } = useLocations();
  const location = locations.find(loc => loc.id === locationId);
  const isStarred = location?.starred || false;

  const handleClick = async (e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent triggering parent click events
    
    try {
      await toggleStar(locationId);
    } catch (error) {
      console.error('Failed to toggle star:', error);
    }
  };

  return (
    <button
      onClick={handleClick}
      className={`star-button ${isStarred ? 'starred' : ''} ${className || ''}`}
      aria-label={isStarred ? 'Unstar location' : 'Star location'}
      title={isStarred ? 'Remove from favorites' : 'Add to favorites'}
    >
      <span className="star-icon">{isStarred ? '★' : '☆'}</span>
    </button>
  );
};

export default StarButton;
```

---

## Benefits of localStorage Approach

### ✅ Advantages:

1. **Persistent** - Data survives page refreshes and browser restarts
2. **No Backend** - Completely client-side
3. **Instant Updates** - No network latency
4. **Works Offline** - No internet required
5. **Shareable** - Via URL parameters
6. **Simple** - Easy to implement and debug
7. **Realistic** - Emulates database behavior
8. **CRUD Operations** - Full create, read, update, delete support

### 📊 Storage Capacity:

- **localStorage limit**: ~5-10MB per domain
- **Our data**: ~15 locations × ~1KB each = ~15KB
- **Plenty of room** for hundreds of locations

### 🔄 Data Persistence:

```
User stars location
  ↓
Update location.starred = true
  ↓
Save to localStorage
  ↓
User closes browser
  ↓
User reopens app
  ↓
Load from localStorage
  ↓
Starred status preserved! ✅
```

---

## Development Tools

### Reset Data (for testing)
```typescript
// Add to window for dev console access
if (import.meta.env.DEV) {
  window.resetLocations = async () => {
    await locationService.resetToInitialData();
    window.location.reload();
  };
}

// In browser console:
// > resetLocations()
```

### View Storage (for debugging)
```typescript
// Add to window for dev console access
if (import.meta.env.DEV) {
  window.viewStorage = () => {
    console.log('Locations:', localStorage.getItem('map-search-locations'));
    console.log('Next ID:', localStorage.getItem('map-search-next-id'));
  };
}

// In browser console:
// > viewStorage()
```

---

## Migration Path

### If You Later Want a Real Backend:

**Step 1**: Keep the same service interface
**Step 2**: Swap implementation:

```typescript
// src/services/locationService.ts

// Development: localStorage
import * as service from './locationService.localStorage';

// Production: Real API
// import * as service from './locationService.api';

export const {
  fetchLocations,
  createLocation,
  updateLocation,
  deleteLocation,
  toggleStarLocation,
  fetchStarredLocations,
} = service;
```

**Step 3**: No changes needed in components! They use the same interface.

---

## Summary

### ✅ localStorage is Perfect for This Project

**Why:**
- Meets all requirements (CRUD, persistence, sharing)
- No backend infrastructure needed
- Realistic database emulation
- Easy to demonstrate
- Simple to implement
- Works great for code exercise

**Implementation:**
- Store locations array in localStorage
- Modify objects to emulate database updates
- Share via URL parameters
- Full CRUD operations supported

This approach provides the best balance of simplicity, functionality, and realism for a code exercise!