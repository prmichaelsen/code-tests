# Zod Schema Architecture

## Overview
Use Zod for runtime validation, type inference, and data transformation. Provides type safety at both compile-time (TypeScript) and runtime (validation).

---

## Why Zod?

### ✅ Benefits:
1. **Runtime Validation** - Catch invalid data from API/localStorage
2. **Type Inference** - Generate TypeScript types from schemas
3. **Parsing** - Transform and coerce data
4. **Error Messages** - Detailed validation errors
5. **Zero Dependencies** - Lightweight (~8KB)
6. **TypeScript-First** - Designed for TypeScript

---

## Installation

```bash
npm install zod
```

---

## Schema Definitions

### File: `src/schemas/location.schema.ts`

```typescript
import { z } from 'zod';

/**
 * Location coordinates schema
 */
export const LocationCoordinatesSchema = z.object({
  lat: z.number().min(-90).max(90),
  lon: z.number().min(-180).max(180),
});

/**
 * Store traffic data schema
 */
export const StoreTrafficSchema = z.object({
  monday: z.number().nullable(),
  tuesday: z.number(),
  wednesday: z.number(),
  thursday: z.number(),
  friday: z.number(),
  saturday: z.number(),
  sunday: z.number(),
}).partial(); // All fields optional

/**
 * Location details schema
 */
export const LocationDetailsSchema = z.object({
  description: z.string().optional(),
  website: z.string().url().optional(),
  avgStoreTraffic: StoreTrafficSchema.optional(),
}).optional();

/**
 * Location schema (main entity)
 */
export const LocationSchema = z.object({
  id: z.number().int().positive(),
  name: z.string().min(1).max(200),
  location: LocationCoordinatesSchema,
  details: LocationDetailsSchema,
  images: z.array(z.string().url()).optional(),
  starred: z.boolean().default(false),
});

/**
 * Array of locations
 */
export const LocationsArraySchema = z.array(LocationSchema);

/**
 * Create location input (without id)
 */
export const CreateLocationSchema = LocationSchema.omit({ id: true, starred: true });

/**
 * Update location input (partial)
 */
export const UpdateLocationSchema = LocationSchema.partial().required({ id: true });

// Infer TypeScript types from schemas
export type Location = z.infer<typeof LocationSchema>;
export type LocationCoordinates = z.infer<typeof LocationCoordinatesSchema>;
export type LocationDetails = z.infer<typeof LocationDetailsSchema>;
export type StoreTraffic = z.infer<typeof StoreTrafficSchema>;
export type CreateLocationInput = z.infer<typeof CreateLocationSchema>;
export type UpdateLocationInput = z.infer<typeof UpdateLocationSchema>;
```

### File: `src/schemas/search.schema.ts`

```typescript
import { z } from 'zod';
import { LocationSchema } from './location.schema';

/**
 * Search query schema
 */
export const SearchQuerySchema = z.object({
  query: z.string().max(200),
  filters: z.object({
    category: z.string().optional(),
    hasImages: z.boolean().optional(),
    starred: z.boolean().optional(),
  }).optional(),
});

/**
 * Search results schema
 */
export const SearchResultsSchema = z.object({
  query: z.string(),
  results: z.array(LocationSchema),
  total: z.number().int().nonnegative(),
});

// Infer types
export type SearchQuery = z.infer<typeof SearchQuerySchema>;
export type SearchResults = z.infer<typeof SearchResultsSchema>;
```

### File: `src/schemas/share.schema.ts`

```typescript
import { z } from 'zod';

/**
 * Create shared list request
 */
export const CreateSharedListSchema = z.object({
  locationIds: z.array(z.number().int().positive()).min(1).max(50),
});

/**
 * Shared list response
 */
export const SharedListResponseSchema = z.object({
  shareId: z.string().length(8),
  url: z.string().url(),
  expiresAt: z.number().int().positive(),
});

/**
 * Shared list data (stored in KV)
 */
export const SharedListDataSchema = z.object({
  locationIds: z.array(z.number().int().positive()),
  createdAt: z.number().int().positive(),
});

// Infer types
export type CreateSharedListInput = z.infer<typeof CreateSharedListSchema>;
export type SharedListResponse = z.infer<typeof SharedListResponseSchema>;
export type SharedListData = z.infer<typeof SharedListDataSchema>;
```

---

## Usage in Services

### File: `src/services/locationService.ts` (Updated)

```typescript
import { Location, LocationSchema, LocationsArraySchema, CreateLocationSchema } from '../schemas/location.schema';
import { initialLocations } from './mockData';
import { getItem, setItem } from './localStorage';

const STORAGE_KEYS = {
  LOCATIONS: 'map-search-locations',
  NEXT_ID: 'map-search-next-id',
};

// Initialize with validated data
function initializeStorage(): void {
  const existing = getItem<unknown[]>(STORAGE_KEYS.LOCATIONS, []);
  
  if (existing.length === 0) {
    // Validate initial data before storing
    const validated = LocationsArraySchema.parse(initialLocations);
    setItem(STORAGE_KEYS.LOCATIONS, validated);
    setItem(STORAGE_KEYS.NEXT_ID, 16);
  }
}

initializeStorage();

function getLocations(): Location[] {
  const data = getItem<unknown[]>(STORAGE_KEYS.LOCATIONS, []);
  
  // Validate data from localStorage
  try {
    return LocationsArraySchema.parse(data);
  } catch (error) {
    console.error('Invalid location data in localStorage:', error);
    // Reset to initial data if corrupted
    setItem(STORAGE_KEYS.LOCATIONS, initialLocations);
    return initialLocations;
  }
}

/**
 * Create new location with validation
 */
export async function createLocation(
  locationData: unknown
): Promise<Location> {
  await delay(300);
  
  // Validate input
  const validated = CreateLocationSchema.parse(locationData);
  
  const locations = getLocations();
  const nextId = getItem<number>(STORAGE_KEYS.NEXT_ID, 16);
  
  const newLocation: Location = {
    ...validated,
    id: nextId,
    starred: false,
  };

  // Validate complete location
  const validatedLocation = LocationSchema.parse(newLocation);
  
  locations.push(validatedLocation);
  saveLocations(locations);
  setItem(STORAGE_KEYS.NEXT_ID, nextId + 1);
  
  return validatedLocation;
}

/**
 * Update location with validation
 */
export async function updateLocation(
  id: number,
  updates: unknown
): Promise<Location> {
  await delay(300);
  
  const locations = getLocations();
  const index = locations.findIndex(loc => loc.id === id);
  if (index === -1) throw new Error(`Location ${id} not found`);

  // Merge and validate
  const updated = { ...locations[index], ...updates };
  const validated = LocationSchema.parse(updated);
  
  locations[index] = validated;
  saveLocations(locations);
  return validated;
}
```

### File: `src/services/shareService.ts` (Updated)

```typescript
import { CreateSharedListSchema, SharedListResponseSchema, SharedListDataSchema } from '../schemas/share.schema';

const API_URL = import.meta.env.VITE_SHARE_API_URL || '/api';

/**
 * Create shared list with validation
 */
export async function createSharedList(locationIds: number[]): Promise<SharedListResponse> {
  // Validate input
  const validated = CreateSharedListSchema.parse({ locationIds });
  
  const response = await fetch(`${API_URL}/share`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(validated),
  });

  if (!response.ok) {
    throw new Error('Failed to create shared list');
  }

  const data = await response.json();
  
  // Validate response
  return SharedListResponseSchema.parse(data);
}

/**
 * Get shared list with validation
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
  
  // Validate response
  const validated = SharedListDataSchema.parse(data);
  return validated.locationIds;
}
```

---

## Cloudflare Worker with Zod

### File: `workers/share-api/src/index.ts`

```typescript
import { z } from 'zod';

export interface Env {
  SHARED_LISTS: KVNamespace;
}

// Schemas
const CreateSharedListSchema = z.object({
  locationIds: z.array(z.number().int().positive()).min(1).max(50),
});

const SharedListDataSchema = z.object({
  locationIds: z.array(z.number().int().positive()),
  createdAt: z.number().int().positive(),
});

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

    // POST /api/share
    if (url.pathname === '/api/share' && request.method === 'POST') {
      try {
        const body = await request.json();
        
        // Validate input with Zod
        const { locationIds } = CreateSharedListSchema.parse(body);
        
        const shareId = crypto.randomUUID().slice(0, 8);
        
        const sharedList = {
          locationIds,
          createdAt: Date.now(),
        };

        // Validate before storing
        const validated = SharedListDataSchema.parse(sharedList);

        await env.SHARED_LISTS.put(
          shareId,
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
      } catch (error) {
        if (error instanceof z.ZodError) {
          return new Response(
            JSON.stringify({ error: 'Invalid input', details: error.errors }),
            { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
          );
        }
        return new Response('Internal Server Error', { status: 500, headers: corsHeaders });
      }
    }

    // GET /api/share/:id
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

      try {
        // Validate data from KV
        const parsed = JSON.parse(data);
        const validated = SharedListDataSchema.parse(parsed);
        
        return new Response(JSON.stringify(validated), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      } catch (error) {
        return new Response('Invalid data', { status: 500, headers: corsHeaders });
      }
    }

    return new Response('Not Found', { status: 404, headers: corsHeaders });
  },
};
```

---

## Form Validation

### File: `src/components/LocationForm/LocationForm.tsx`

```typescript
import { z } from 'zod';
import { CreateLocationSchema } from '@schemas/location.schema';

const LocationForm: React.FC = () => {
  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleSubmit = useCallback(async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    
    const data = {
      name: formData.get('name'),
      location: {
        lat: parseFloat(formData.get('lat') as string),
        lon: parseFloat(formData.get('lon') as string),
      },
      details: {
        description: formData.get('description'),
        website: formData.get('website'),
      },
    };

    try {
      // Validate with Zod
      const validated = CreateLocationSchema.parse(data);
      
      // Create location
      await createLocation(validated);
      
      // Success!
      setErrors({});
      alert('Location created successfully!');
    } catch (error) {
      if (error instanceof z.ZodError) {
        // Convert Zod errors to form errors
        const formErrors: Record<string, string> = {};
        error.errors.forEach(err => {
          const path = err.path.join('.');
          formErrors[path] = err.message;
        });
        setErrors(formErrors);
      }
    }
  }, []);

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Name</label>
        <input name="name" required />
        {errors.name && <span className="error">{errors.name}</span>}
      </div>

      <div>
        <label>Latitude</label>
        <input name="lat" type="number" step="any" required />
        {errors['location.lat'] && <span className="error">{errors['location.lat']}</span>}
      </div>

      <div>
        <label>Longitude</label>
        <input name="lon" type="number" step="any" required />
        {errors['location.lon'] && <span className="error">{errors['location.lon']}</span>}
      </div>

      <div>
        <label>Description</label>
        <textarea name="description" />
        {errors['details.description'] && <span className="error">{errors['details.description']}</span>}
      </div>

      <div>
        <label>Website</label>
        <input name="website" type="url" />
        {errors['details.website'] && <span className="error">{errors['details.website']}</span>}
      </div>

      <button type="submit">Create Location</button>
    </form>
  );
};
```

---

## Data Transformation

### Parsing localStorage Data

```typescript
import { LocationsArraySchema } from '@schemas/location.schema';

function getLocations(): Location[] {
  const data = getItem<unknown[]>(STORAGE_KEYS.LOCATIONS, []);
  
  try {
    // Parse and validate
    return LocationsArraySchema.parse(data);
  } catch (error) {
    if (error instanceof z.ZodError) {
      console.error('Invalid location data:', error.errors);
    }
    // Reset to initial data if corrupted
    return initialLocations;
  }
}
```

### Parsing API Responses

```typescript
import { LocationSchema } from '@schemas/location.schema';

export async function fetchLocationById(id: number): Promise<Location> {
  const response = await fetch(`/api/locations/${id}`);
  const data = await response.json();
  
  // Validate API response
  return LocationSchema.parse(data);
}
```

### Coercing Form Data

```typescript
// Automatically convert strings to numbers
const CoordinatesSchema = z.object({
  lat: z.coerce.number().min(-90).max(90),
  lon: z.coerce.number().min(-180).max(180),
});

// "42.354022" → 42.354022 (number)
const coords = CoordinatesSchema.parse({
  lat: "42.354022",
  lon: "-71.046245"
});
```

---

## Custom Validation

### File: `src/schemas/location.schema.ts` (Enhanced)

```typescript
/**
 * Location schema with custom validations
 */
export const LocationSchema = z.object({
  id: z.number().int().positive(),
  name: z.string()
    .min(1, 'Name is required')
    .max(200, 'Name must be less than 200 characters')
    .trim(),
  location: z.object({
    lat: z.number()
      .min(-90, 'Latitude must be between -90 and 90')
      .max(90, 'Latitude must be between -90 and 90'),
    lon: z.number()
      .min(-180, 'Longitude must be between -180 and 180')
      .max(180, 'Longitude must be between -180 and 180'),
  }),
  details: z.object({
    description: z.string()
      .max(1000, 'Description must be less than 1000 characters')
      .optional(),
    website: z.string()
      .url('Must be a valid URL')
      .optional()
      .or(z.literal('')), // Allow empty string
    avgStoreTraffic: z.object({
      monday: z.number().int().nonnegative().nullable(),
      tuesday: z.number().int().nonnegative(),
      wednesday: z.number().int().nonnegative(),
      thursday: z.number().int().nonnegative(),
      friday: z.number().int().nonnegative(),
      saturday: z.number().int().nonnegative(),
      sunday: z.number().int().nonnegative(),
    }).partial().optional(),
  }).optional(),
  images: z.array(
    z.string().url('Each image must be a valid URL')
  ).max(10, 'Maximum 10 images allowed').optional(),
  starred: z.boolean().default(false),
})
  .refine(
    (data) => {
      // Custom validation: Boston area check
      const bostonLat = 42.3601;
      const bostonLon = -71.0589;
      const maxDistance = 0.5; // ~50km radius
      
      const distance = Math.sqrt(
        Math.pow(data.location.lat - bostonLat, 2) +
        Math.pow(data.location.lon - bostonLon, 2)
      );
      
      return distance <= maxDistance;
    },
    { message: 'Location must be in the Boston area' }
  );
```

---

## Type Safety Benefits

### Before (Just TypeScript):

```typescript
// ❌ No runtime validation
interface Location {
  id: number;
  name: string;
  // ...
}

// This compiles but could fail at runtime
const location: Location = JSON.parse(localStorage.getItem('location'));
// What if data is corrupted? null? wrong shape?
```

### After (With Zod):

```typescript
// ✅ Runtime validation + type inference
const LocationSchema = z.object({
  id: z.number(),
  name: z.string(),
  // ...
});

type Location = z.infer<typeof LocationSchema>;

// This validates at runtime
const location = LocationSchema.parse(JSON.parse(localStorage.getItem('location')));
// Throws if invalid, guarantees correct shape
```

---

## Error Handling

### Graceful Degradation

```typescript
function getLocations(): Location[] {
  const data = getItem<unknown[]>(STORAGE_KEYS.LOCATIONS, []);
  
  // Try to parse with Zod
  const result = LocationsArraySchema.safeParse(data);
  
  if (result.success) {
    return result.data;
  } else {
    // Log errors
    console.error('Invalid location data:', result.error.errors);
    
    // Reset to initial data
    setItem(STORAGE_KEYS.LOCATIONS, initialLocations);
    return initialLocations;
  }
}
```

### User-Friendly Error Messages

```typescript
try {
  const validated = CreateLocationSchema.parse(formData);
} catch (error) {
  if (error instanceof z.ZodError) {
    // Format errors for users
    const messages = error.errors.map(err => {
      const field = err.path.join('.');
      return `${field}: ${err.message}`;
    });
    
    alert(`Validation errors:\n${messages.join('\n')}`);
  }
}
```

---

## Schema Composition

### Reusable Schemas

```typescript
// Base schemas
const UrlSchema = z.string().url();
const PositiveIntSchema = z.number().int().positive();
const NonEmptyStringSchema = z.string().min(1);

// Compose into complex schemas
const LocationSchema = z.object({
  id: PositiveIntSchema,
  name: NonEmptyStringSchema.max(200),
  details: z.object({
    website: UrlSchema.optional(),
  }).optional(),
});
```

### Schema Transformations

```typescript
// Transform data during parsing
const LocationSchema = z.object({
  name: z.string().trim().toLowerCase(), // Auto-transform
  location: z.object({
    lat: z.coerce.number(), // Auto-convert string to number
    lon: z.coerce.number(),
  }),
  starred: z.boolean().default(false), // Auto-add default
});
```

---

## Testing with Zod

### File: `src/schemas/location.schema.test.ts`

```typescript
import { describe, it, expect } from 'vitest';
import { LocationSchema, CreateLocationSchema } from './location.schema';

describe('LocationSchema', () => {
  it('validates correct location', () => {
    const valid = {
      id: 1,
      name: 'Test Location',
      location: { lat: 42.354022, lon: -71.046245 },
      starred: false,
    };

    expect(() => LocationSchema.parse(valid)).not.toThrow();
  });

  it('rejects invalid latitude', () => {
    const invalid = {
      id: 1,
      name: 'Test',
      location: { lat: 100, lon: -71.046245 }, // Invalid: > 90
      starred: false,
    };

    expect(() => LocationSchema.parse(invalid)).toThrow();
  });

  it('requires name', () => {
    const invalid = {
      id: 1,
      name: '', // Empty name
      location: { lat: 42, lon: -71 },
    };

    expect(() => LocationSchema.parse(invalid)).toThrow();
  });
});
```

---

## Package.json Update

```json
{
  "dependencies": {
    "zod": "^3.22.4",
    "@react-google-maps/api": "^2.19.2",
    "chart.js": "^4.4.1",
    "react-chartjs-2": "^5.2.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }
}
```

---

## Benefits Summary

### ✅ Runtime Safety:
- Catch invalid data from localStorage
- Validate API responses
- Prevent corrupted data
- Type-safe at runtime

### ✅ Developer Experience:
- Type inference (no duplicate types)
- Autocomplete in IDE
- Compile-time + runtime checks
- Clear error messages

### ✅ Data Quality:
- Enforce constraints (min/max, format)
- Transform data automatically
- Validate before storing
- Graceful error handling

### ✅ Maintainability:
- Single source of truth for schemas
- Easy to update validation rules
- Self-documenting code
- Easier testing

---

## File Structure

```
src/
├── schemas/
│   ├── location.schema.ts     # Location entity schemas
│   ├── search.schema.ts       # Search-related schemas
│   ├── share.schema.ts        # Sharing schemas
│   └── index.ts               # Re-export all schemas
├── services/
│   ├── locationService.ts     # Uses schemas for validation
│   ├── shareService.ts        # Uses schemas for validation
│   └── localStorage.ts
└── types/
    └── index.ts               # Re-export inferred types
```

---

## Summary

### ✅ Zod Integration:

**Schemas replace TypeScript interfaces:**
- Define once with Zod
- Infer TypeScript types
- Get runtime validation

**Use everywhere:**
- localStorage operations
- API requests/responses
- Form validation
- Cloudflare Worker
- Data transformation

**Benefits:**
- Type-safe at compile-time AND runtime
- Catch bugs early
- Better error messages
- Self-documenting code

This provides robust data validation throughout the entire application!