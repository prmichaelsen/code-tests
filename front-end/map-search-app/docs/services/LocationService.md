# Location Service Architecture

## Overview
A service layer that abstracts data access for location operations. Provides a clean API for CRUD operations and can switch between mock data and real API seamlessly.

---

## Service Interface

### File: `src/services/locationService.ts`

```typescript
import { Location } from '../types/location.types';

/**
 * Fetch all locations
 * @returns Promise<Location[]>
 */
export async function fetchLocations(): Promise<Location[]>;

/**
 * Fetch a single location by ID
 * @param id - Location ID
 * @returns Promise<Location>
 */
export async function fetchLocationById(id: number): Promise<Location>;

/**
 * Search locations by query
 * @param query - Search query string
 * @returns Promise<Location[]>
 */
export async function searchLocations(query: string): Promise<Location[]>;

/**
 * Create a new location
 * @param location - Location data without ID
 * @returns Promise<Location> - Created location with ID
 */
export async function createLocation(
  location: Omit<Location, 'id'>
): Promise<Location>;

/**
 * Update an existing location
 * @param id - Location ID
 * @param updates - Partial location data to update
 * @returns Promise<Location> - Updated location
 */
export async function updateLocation(
  id: number,
  updates: Partial<Location>
): Promise<Location>;

/**
 * Delete a location
 * @param id - Location ID
 * @returns Promise<void>
 */
export async function deleteLocation(id: number): Promise<void>;

/**
 * Toggle star/favorite status
 * @param id - Location ID
 * @returns Promise<Location> - Updated location
 */
export async function toggleStarLocation(id: number): Promise<Location>;
```

---

## Implementation Strategies

### Strategy 1: Mock Data (Development)

**File: `src/services/mockData.ts`**

```typescript
import { Location } from '../types/location.types';

// Convert sample-data.js to TypeScript
export const mockLocations: Location[] = [
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
  // ... rest of locations
];

// In-memory storage for development
let locations = [...mockLocations];
let nextId = Math.max(...locations.map(l => l.id)) + 1;
```

**File: `src/services/locationService.ts`** (Mock Implementation)

```typescript
import { Location } from '../types/location.types';
import { mockLocations } from './mockData';

// In-memory storage
let locations = [...mockLocations];
let nextId = Math.max(...locations.map(l => l.id)) + 1;

// Simulate network delay
const delay = (ms: number = 300) => new Promise(resolve => setTimeout(resolve, ms));

export async function fetchLocations(): Promise<Location[]> {
  await delay();
  return [...locations];
}

export async function fetchLocationById(id: number): Promise<Location> {
  await delay();
  const location = locations.find(loc => loc.id === id);
  if (!location) {
    throw new Error(`Location with id ${id} not found`);
  }
  return { ...location };
}

export async function searchLocations(query: string): Promise<Location[]> {
  await delay(200);
  const lowerQuery = query.toLowerCase().trim();
  
  if (!lowerQuery) return [];

  return locations.filter(location =>
    location.name.toLowerCase().includes(lowerQuery) ||
    location.details?.description?.toLowerCase().includes(lowerQuery)
  );
}

export async function createLocation(
  locationData: Omit<Location, 'id'>
): Promise<Location> {
  await delay();
  
  const newLocation: Location = {
    ...locationData,
    id: nextId++,
    starred: false,
  };

  locations.push(newLocation);
  return { ...newLocation };
}

export async function updateLocation(
  id: number,
  updates: Partial<Location>
): Promise<Location> {
  await delay();
  
  const index = locations.findIndex(loc => loc.id === id);
  if (index === -1) {
    throw new Error(`Location with id ${id} not found`);
  }

  locations[index] = { ...locations[index], ...updates };
  return { ...locations[index] };
}

export async function deleteLocation(id: number): Promise<void> {
  await delay();
  
  const index = locations.findIndex(loc => loc.id === id);
  if (index === -1) {
    throw new Error(`Location with id ${id} not found`);
  }

  locations.splice(index, 1);
}

export async function toggleStarLocation(id: number): Promise<Location> {
  await delay();
  
  const location = locations.find(loc => loc.id === id);
  if (!location) {
    throw new Error(`Location with id ${id} not found`);
  }

  location.starred = !location.starred;
  return { ...location };
}
```

---

### Strategy 2: JSON Server (Mock API)

**File: `db.json`** (project root)

```json
{
  "locations": [
    {
      "id": 1,
      "name": "Alberts Bike Shop",
      "location": {
        "lat": 42.354022,
        "lon": -71.046245
      },
      "details": {
        "description": "We buy and sell used bikes and equipment.",
        "website": "https://groundsignal.com"
      },
      "images": [
        "http://dspncdn.com/a1/media/692x/f8/58/77/f85877c41fb6147599886048e3582d47.jpg"
      ],
      "starred": false
    }
  ]
}
```

**Start JSON Server:**
```bash
npx json-server --watch db.json --port 3001
```

**File: `src/services/api.ts`**

```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3001';

interface FetchOptions extends RequestInit {
  timeout?: number;
}

class ApiClient {
  private baseURL: string;
  private defaultTimeout: number;

  constructor(baseURL: string, timeout = 10000) {
    this.baseURL = baseURL;
    this.defaultTimeout = timeout;
  }

  private async fetchWithTimeout(
    url: string,
    options: FetchOptions = {}
  ): Promise<Response> {
    const { timeout = this.defaultTimeout, ...fetchOptions } = options;

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
      const response = await fetch(url, {
        ...fetchOptions,
        signal: controller.signal,
      });
      clearTimeout(timeoutId);
      return response;
    } catch (error) {
      clearTimeout(timeoutId);
      throw error;
    }
  }

  async get<T>(endpoint: string): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    const response = await this.fetchWithTimeout(url);
    
    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status}`);
    }
    
    return response.json();
  }

  async post<T>(endpoint: string, data: any): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    const response = await this.fetchWithTimeout(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    
    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status}`);
    }
    
    return response.json();
  }

  async put<T>(endpoint: string, data: any): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    const response = await this.fetchWithTimeout(url, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    
    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status}`);
    }
    
    return response.json();
  }

  async delete(endpoint: string): Promise<void> {
    const url = `${this.baseURL}${endpoint}`;
    const response = await this.fetchWithTimeout(url, {
      method: 'DELETE',
    });
    
    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status}`);
    }
  }
}

export const apiClient = new ApiClient(API_BASE_URL);
```

**File: `src/services/locationService.ts`** (API Implementation)

```typescript
import { apiClient } from './api';
import { Location } from '../types/location.types';

const ENDPOINTS = {
  LOCATIONS: '/locations',
};

export async function fetchLocations(): Promise<Location[]> {
  return apiClient.get<Location[]>(ENDPOINTS.LOCATIONS);
}

export async function fetchLocationById(id: number): Promise<Location> {
  return apiClient.get<Location>(`${ENDPOINTS.LOCATIONS}/${id}`);
}

export async function searchLocations(query: string): Promise<Location[]> {
  // JSON Server supports query parameters
  return apiClient.get<Location[]>(`${ENDPOINTS.LOCATIONS}?q=${encodeURIComponent(query)}`);
}

export async function createLocation(
  location: Omit<Location, 'id'>
): Promise<Location> {
  return apiClient.post<Location>(ENDPOINTS.LOCATIONS, location);
}

export async function updateLocation(
  id: number,
  updates: Partial<Location>
): Promise<Location> {
  return apiClient.put<Location>(`${ENDPOINTS.LOCATIONS}/${id}`, updates);
}

export async function deleteLocation(id: number): Promise<void> {
  return apiClient.delete(`${ENDPOINTS.LOCATIONS}/${id}`);
}

export async function toggleStarLocation(id: number): Promise<Location> {
  const location = await fetchLocationById(id);
  return updateLocation(id, { starred: !location.starred });
}
```

---

### Strategy 3: Custom Express API (Production-Ready)

**File: `api/server.ts`** (separate API project)

```typescript
import express from 'express';
import cors from 'cors';
import { mockLocations } from './data';

const app = express();
const PORT = 3001;

app.use(cors());
app.use(express.json());

let locations = [...mockLocations];
let nextId = Math.max(...locations.map(l => l.id)) + 1;

// GET /api/locations - Fetch all locations
app.get('/api/locations', (req, res) => {
  const { q } = req.query;
  
  if (q && typeof q === 'string') {
    const query = q.toLowerCase();
    const filtered = locations.filter(loc =>
      loc.name.toLowerCase().includes(query) ||
      loc.details?.description?.toLowerCase().includes(query)
    );
    return res.json(filtered);
  }
  
  res.json(locations);
});

// GET /api/locations/:id - Fetch single location
app.get('/api/locations/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const location = locations.find(loc => loc.id === id);
  
  if (!location) {
    return res.status(404).json({ error: 'Location not found' });
  }
  
  res.json(location);
});

// POST /api/locations - Create new location
app.post('/api/locations', (req, res) => {
  const newLocation = {
    ...req.body,
    id: nextId++,
    starred: false,
  };
  
  locations.push(newLocation);
  res.status(201).json(newLocation);
});

// PUT /api/locations/:id - Update location
app.put('/api/locations/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const index = locations.findIndex(loc => loc.id === id);
  
  if (index === -1) {
    return res.status(404).json({ error: 'Location not found' });
  }
  
  locations[index] = { ...locations[index], ...req.body, id };
  res.json(locations[index]);
});

// PATCH /api/locations/:id - Partial update
app.patch('/api/locations/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const index = locations.findIndex(loc => loc.id === id);
  
  if (index === -1) {
    return res.status(404).json({ error: 'Location not found' });
  }
  
  locations[index] = { ...locations[index], ...req.body };
  res.json(locations[index]);
});

// DELETE /api/locations/:id - Delete location
app.delete('/api/locations/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const index = locations.findIndex(loc => loc.id === id);
  
  if (index === -1) {
    return res.status(404).json({ error: 'Location not found' });
  }
  
  locations.splice(index, 1);
  res.status(204).send();
});

// POST /api/locations/:id/star - Toggle star
app.post('/api/locations/:id/star', (req, res) => {
  const id = parseInt(req.params.id);
  const location = locations.find(loc => loc.id === id);
  
  if (!location) {
    return res.status(404).json({ error: 'Location not found' });
  }
  
  location.starred = !location.starred;
  res.json(location);
});

app.listen(PORT, () => {
  console.log(`API server running on http://localhost:${PORT}`);
});
```

---

## Service Configuration

### Environment-Based Strategy Selection

**File: `src/services/locationService.ts`**

```typescript
import { Location } from '../types/location.types';

// Determine which implementation to use
const USE_MOCK_DATA = import.meta.env.VITE_USE_MOCK_DATA === 'true';

// Import appropriate implementation
const service = USE_MOCK_DATA
  ? await import('./locationService.mock')
  : await import('./locationService.api');

// Re-export all functions
export const {
  fetchLocations,
  fetchLocationById,
  searchLocations,
  createLocation,
  updateLocation,
  deleteLocation,
  toggleStarLocation,
} = service;
```

---

## API Endpoints

### RESTful API Design

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| GET | `/locations` | List all locations | - | `Location[]` |
| GET | `/locations?q={query}` | Search locations | - | `Location[]` |
| GET | `/locations/:id` | Get single location | - | `Location` |
| POST | `/locations` | Create location | `Omit<Location, 'id'>` | `Location` |
| PUT | `/locations/:id` | Update location | `Partial<Location>` | `Location` |
| DELETE | `/locations/:id` | Delete location | - | `204 No Content` |
| POST | `/locations/:id/star` | Toggle star | - | `Location` |

---

## Request/Response Examples

### GET /locations
```typescript
// Request
GET /locations

// Response
[
  {
    "id": 1,
    "name": "Alberts Bike Shop",
    "location": { "lat": 42.354022, "lon": -71.046245 },
    "details": { ... },
    "images": [...],
    "starred": false
  },
  ...
]
```

### GET /locations?q=bike
```typescript
// Request
GET /locations?q=bike

// Response (filtered)
[
  {
    "id": 1,
    "name": "Alberts Bike Shop",
    ...
  }
]
```

### POST /locations
```typescript
// Request
POST /locations
Content-Type: application/json

{
  "name": "New Coffee Shop",
  "location": { "lat": 42.360000, "lon": -71.060000 },
  "details": {
    "description": "Best coffee in town",
    "website": "https://example.com"
  },
  "images": []
}

// Response
{
  "id": 16,
  "name": "New Coffee Shop",
  "location": { "lat": 42.360000, "lon": -71.060000 },
  "details": { ... },
  "images": [],
  "starred": false
}
```

### PUT /locations/1
```typescript
// Request
PUT /locations/1
Content-Type: application/json

{
  "name": "Alberts Bike Shop - Updated",
  "details": {
    "description": "New description"
  }
}

// Response
{
  "id": 1,
  "name": "Alberts Bike Shop - Updated",
  "location": { "lat": 42.354022, "lon": -71.046245 },
  "details": {
    "description": "New description",
    "website": "https://groundsignal.com"
  },
  ...
}
```

### DELETE /locations/1
```typescript
// Request
DELETE /locations/1

// Response
204 No Content
```

---

## Error Handling

```typescript
export class LocationServiceError extends Error {
  constructor(
    message: string,
    public statusCode?: number,
    public originalError?: Error
  ) {
    super(message);
    this.name = 'LocationServiceError';
  }
}

// Wrap API calls with error handling
async function fetchLocations(): Promise<Location[]> {
  try {
    return await apiClient.get<Location[]>('/locations');
  } catch (error) {
    if (error instanceof Error) {
      throw new LocationServiceError(
        'Failed to fetch locations',
        500,
        error
      );
    }
    throw error;
  }
}
```

---

## Caching Strategy (Optional)

```typescript
class LocationCache {
  private cache = new Map<string, { data: any; timestamp: number }>();
  private ttl = 5 * 60 * 1000; // 5 minutes

  get<T>(key: string): T | null {
    const cached = this.cache.get(key);
    if (!cached) return null;

    const isExpired = Date.now() - cached.timestamp > this.ttl;
    if (isExpired) {
      this.cache.delete(key);
      return null;
    }

    return cached.data as T;
  }

  set(key: string, data: any): void {
    this.cache.set(key, { data, timestamp: Date.now() });
  }

  clear(): void {
    this.cache.clear();
  }
}

const cache = new LocationCache();

export async function fetchLocations(): Promise<Location[]> {
  const cached = cache.get<Location[]>('locations');
  if (cached) return cached;

  const locations = await apiClient.get<Location[]>('/locations');
  cache.set('locations', locations);
  return locations;
}
```

---

## Testing

### Mock Service Tests
```typescript
import { fetchLocations, createLocation, deleteLocation } from './locationService';

describe('LocationService', () => {
  it('fetches all locations', async () => {
    const locations = await fetchLocations();
    expect(locations).toHaveLength(15);
  });

  it('creates a new location', async () => {
    const newLocation = await createLocation({
      name: 'Test Location',
      location: { lat: 42.0, lon: -71.0 },
    });
    expect(newLocation.id).toBeDefined();
    expect(newLocation.name).toBe('Test Location');
  });

  it('deletes a location', async () => {
    await deleteLocation(1);
    const locations = await fetchLocations();
    expect(locations.find(l => l.id === 1)).toBeUndefined();
  });
});
```

---

## File Structure

```
src/services/
├── api.ts                    # HTTP client (native fetch)
├── locationService.ts        # Main service interface
├── locationService.mock.ts   # Mock implementation
├── locationService.api.ts    # API implementation
└── mockData.ts               # Sample data from sample-data.js
```

---

## Usage in Components

```typescript
import { fetchLocations, createLocation } from '@services/locationService';

// In LocationContext
useEffect(() => {
  const loadLocations = async () => {
    try {
      const data = await fetchLocations();
      setLocations(data);
    } catch (error) {
      console.error('Failed to load locations:', error);
    }
  };

  loadLocations();
}, []);

// In a form component
const handleSubmit = async (formData: LocationFormData) => {
  try {
    const newLocation = await createLocation(formData);
    // Update context
    addLocation(newLocation);
  } catch (error) {
    console.error('Failed to create location:', error);
  }
};
```

---

## Benefits of This Architecture

### ✅ Separation of Concerns
- Business logic separated from UI
- Easy to test independently
- Clear API contracts

### ✅ Flexibility
- Switch between mock and real API easily
- Environment-based configuration
- Easy to add caching or other features

### ✅ Type Safety
- Full TypeScript support
- Compile-time error checking
- IntelliSense support

### ✅ Maintainability
- Single source of truth for data operations
- Easy to add new endpoints
- Consistent error handling

---

## Recommended Approach

**For Development**: Use **Mock Data** (Strategy 1)
- Fastest to implement
- No external dependencies
- Perfect for prototyping

**For Demo**: Use **JSON Server** (Strategy 2)
- Realistic API behavior
- Persistent data during session
- Easy to set up

**For Production**: Use **Real API** (Strategy 3)
- Cloudflare Workers
- Firebase
- Your own backend

---

## Summary

The service layer provides:
- ✅ Clean abstraction over data access
- ✅ Easy switching between mock and real data
- ✅ Type-safe operations
- ✅ Error handling
- ✅ Consistent API
- ✅ Testable code

Start with mock data, then migrate to JSON Server or real API as needed.