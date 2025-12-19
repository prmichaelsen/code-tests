# DTO Naming Strategy and Schema Organization

## Overview
Clear naming conventions for DTOs (Data Transfer Objects) that indicate the service layer, direction (request/response), and purpose.

---

## Naming Convention

### Pattern: `{Service}{Entity}{Direction}{Purpose?}`

**Examples:**
- `ApiLocationResponse` - Location from API
- `ApiCreateLocationRequest` - Create location request to API
- `KvUserStarData` - User star data stored in KV
- `KvSharedListData` - Shared list stored in KV
- `LocalStorageUserPreferences` - User preferences in localStorage

---

## Schema Organization by Service Layer

### File Structure:

```
src/schemas/
├── api/                        # API request/response DTOs
│   ├── location.api.schema.ts
│   ├── star.api.schema.ts
│   └── share.api.schema.ts
├── kv/                         # Cloudflare KV storage DTOs
│   ├── user.kv.schema.ts
│   └── share.kv.schema.ts
├── local/                      # localStorage DTOs
│   └── preferences.local.schema.ts
├── domain/                     # Domain entities (shared)
│   └── location.domain.schema.ts
└── index.ts                    # Re-exports
```

---

## Domain Schemas (Shared Entities)

### File: `src/schemas/domain/location.domain.schema.ts`

```typescript
import { z } from 'zod';

/**
 * Core domain entity - used across all layers
 */
export const LocationDomainSchema = z.object({
  id: z.number().int().positive(),
  name: z.string().min(1).max(200).trim(),
  location: z.object({
    lat: z.number().min(-90).max(90),
    lon: z.number().min(-180).max(180),
  }),
  details: z.object({
    description: z.string().max(1000).optional(),
    website: z.string().url().optional().or(z.literal('')),
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
  images: z.array(z.string().url()).max(10).optional(),
  starred: z.boolean().default(false),
});

export type LocationDomain = z.infer<typeof LocationDomainSchema>;
```

---

## API Layer Schemas (Client ↔ Worker)

### File: `src/schemas/api/location.api.schema.ts`

```typescript
import { z } from 'zod';
import { LocationDomainSchema } from '../domain/location.domain.schema';

/**
 * API Response: Get all locations
 * GET /api/locations
 */
export const ApiGetLocationsResponseSchema = z.object({
  locations: z.array(LocationDomainSchema),
  total: z.number().int().nonnegative(),
});

/**
 * API Request: Create location
 * POST /api/locations
 */
export const ApiCreateLocationRequestSchema = LocationDomainSchema.omit({
  id: true,
  starred: true,
});

/**
 * API Response: Create location
 * POST /api/locations
 */
export const ApiCreateLocationResponseSchema = LocationDomainSchema;

/**
 * API Request: Update location
 * PUT /api/locations/:id
 */
export const ApiUpdateLocationRequestSchema = LocationDomainSchema
  .partial()
  .required({ id: true });

/**
 * API Response: Update location
 * PUT /api/locations/:id
 */
export const ApiUpdateLocationResponseSchema = LocationDomainSchema;

/**
 * API Response: Delete location
 * DELETE /api/locations/:id
 */
export const ApiDeleteLocationResponseSchema = z.object({
  success: z.boolean(),
  id: z.number().int().positive(),
});

// Infer types
export type ApiGetLocationsResponse = z.infer<typeof ApiGetLocationsResponseSchema>;
export type ApiCreateLocationRequest = z.infer<typeof ApiCreateLocationRequestSchema>;
export type ApiCreateLocationResponse = z.infer<typeof ApiCreateLocationResponseSchema>;
export type ApiUpdateLocationRequest = z.infer<typeof ApiUpdateLocationRequestSchema>;
export type ApiUpdateLocationResponse = z.infer<typeof ApiUpdateLocationResponseSchema>;
export type ApiDeleteLocationResponse = z.infer<typeof ApiDeleteLocationResponseSchema>;
```

### File: `src/schemas/api/star.api.schema.ts`

```typescript
import { z } from 'zod';

/**
 * API Response: Get user's starred locations
 * GET /api/users/:userId/starred
 */
export const ApiGetStarredResponseSchema = z.object({
  userId: z.string().uuid(),
  starredLocationIds: z.array(z.number().int().positive()),
  updatedAt: z.number().int().positive(),
});

/**
 * API Response: Toggle star
 * POST /api/users/:userId/starred/:locationId
 */
export const ApiToggleStarResponseSchema = z.object({
  userId: z.string().uuid(),
  locationId: z.number().int().positive(),
  starred: z.boolean(),
  starredLocationIds: z.array(z.number().int().positive()),
  updatedAt: z.number().int().positive(),
});

/**
 * API Request: Star multiple locations
 * POST /api/users/:userId/starred/bulk
 */
export const ApiStarBulkRequestSchema = z.object({
  locationIds: z.array(z.number().int().positive()).min(1).max(50),
});

/**
 * API Response: Star multiple locations
 * POST /api/users/:userId/starred/bulk
 */
export const ApiStarBulkResponseSchema = z.object({
  userId: z.string().uuid(),
  starredLocationIds: z.array(z.number().int().positive()),
  addedCount: z.number().int().nonnegative(),
  updatedAt: z.number().int().positive(),
});

// Infer types
export type ApiGetStarredResponse = z.infer<typeof ApiGetStarredResponseSchema>;
export type ApiToggleStarResponse = z.infer<typeof ApiToggleStarResponseSchema>;
export type ApiStarBulkRequest = z.infer<typeof ApiStarBulkRequestSchema>;
export type ApiStarBulkResponse = z.infer<typeof ApiStarBulkResponseSchema>;
```

### File: `src/schemas/api/share.api.schema.ts`

```typescript
import { z } from 'zod';

/**
 * API Request: Create shared list
 * POST /api/share
 */
export const ApiCreateShareRequestSchema = z.object({
  userId: z.string().uuid(),
  locationIds: z.array(z.number().int().positive()).min(1).max(50),
});

/**
 * API Response: Create shared list
 * POST /api/share
 */
export const ApiCreateShareResponseSchema = z.object({
  shareId: z.string().length(8),
  url: z.string().url(),
  expiresAt: z.number().int().positive(),
});

/**
 * API Response: Get shared list
 * GET /api/share/:shareId
 */
export const ApiGetShareResponseSchema = z.object({
  shareId: z.string(),
  userId: z.string().uuid(),
  locationIds: z.array(z.number().int().positive()),
  createdAt: z.number().int().positive(),
});

// Infer types
export type ApiCreateShareRequest = z.infer<typeof ApiCreateShareRequestSchema>;
export type ApiCreateShareResponse = z.infer<typeof ApiCreateShareResponseSchema>;
export type ApiGetShareResponse = z.infer<typeof ApiGetShareResponseSchema>;
```

---

## KV Layer Schemas (Worker Storage)

### File: `src/schemas/kv/user.kv.schema.ts`

```typescript
import { z } from 'zod';

/**
 * KV Storage: User star data
 * Key: user:{userId}
 * Value: KvUserStarData
 */
export const KvUserStarDataSchema = z.object({
  userId: z.string().uuid(),
  starredLocationIds: z.array(z.number().int().positive()),
  createdAt: z.number().int().positive(),
  updatedAt: z.number().int().positive(),
});

export type KvUserStarData = z.infer<typeof KvUserStarDataSchema>;
```

### File: `src/schemas/kv/share.kv.schema.ts`

```typescript
import { z } from 'zod';

/**
 * KV Storage: Shared list data
 * Key: share:{shareId}
 * Value: KvSharedListData
 * TTL: 30 days
 */
export const KvSharedListDataSchema = z.object({
  shareId: z.string().length(8),
  userId: z.string().uuid(),
  locationIds: z.array(z.number().int().positive()),
  createdAt: z.number().int().positive(),
});

export type KvSharedListData = z.infer<typeof KvSharedListDataSchema>;
```

---

## localStorage Schemas (Client Storage)

### File: `src/schemas/local/preferences.local.schema.ts`

```typescript
import { z } from 'zod';

/**
 * localStorage: User preferences
 * Key: map-search-preferences
 * Value: LocalStorageUserPreferences
 */
export const LocalStorageUserPreferencesSchema = z.object({
  userId: z.string().uuid(),
  theme: z.enum(['light', 'dark']).default('light'),
  mapStyle: z.enum(['default', 'satellite', 'terrain']).default('default'),
  lastVisited: z.number().int().positive(),
});

export type LocalStorageUserPreferences = z.infer<typeof LocalStorageUserPreferencesSchema>;
```

---

## Service Layer Usage

### File: `src/services/starService.ts` (Updated)

```typescript
import {
  ApiGetStarredResponse,
  ApiGetStarredResponseSchema,
  ApiToggleStarResponse,
  ApiToggleStarResponseSchema,
  ApiStarBulkRequest,
  ApiStarBulkResponse,
  ApiStarBulkRequestSchema,
  ApiStarBulkResponseSchema,
} from '../schemas/api/star.api.schema';

const API_URL = import.meta.env.VITE_API_URL || '/api';

/**
 * Fetch user's starred location IDs
 */
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

/**
 * Toggle star status
 */
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

/**
 * Star multiple locations
 */
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

### File: `src/services/shareService.ts` (Updated)

```typescript
import {
  ApiCreateShareRequest,
  ApiCreateShareRequestSchema,
  ApiCreateShareResponse,
  ApiCreateShareResponseSchema,
  ApiGetShareResponse,
  ApiGetShareResponseSchema,
} from '../schemas/api/share.api.schema';

const API_URL = import.meta.env.VITE_API_URL || '/api';

/**
 * Create a shareable list
 */
export async function createSharedList(
  userId: string,
  locationIds: number[]
): Promise<ApiCreateShareResponse> {
  // Validate request
  const request: ApiCreateShareRequest = ApiCreateShareRequestSchema.parse({
    userId,
    locationIds,
  });
  
  const response = await fetch(`${API_URL}/share`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error('Failed to create shared list');
  }

  const data: unknown = await response.json();
  return ApiCreateShareResponseSchema.parse(data);
}

/**
 * Get a shared list
 */
export async function getSharedList(shareId: string): Promise<ApiGetShareResponse> {
  const response = await fetch(`${API_URL}/share/${shareId}`);

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Shared list not found or expired');
    }
    throw new Error('Failed to fetch shared list');
  }

  const data: unknown = await response.json();
  return ApiGetShareResponseSchema.parse(data);
}
```

---

## Cloudflare Worker Schemas

### File: `workers/api/src/schemas/kv.schemas.ts`

```typescript
import { z } from 'zod';

/**
 * KV Storage: User star data
 * Key pattern: user:{userId}
 * TTL: Never expires
 */
export const KvUserStarDataSchema = z.object({
  userId: z.string().uuid(),
  starredLocationIds: z.array(z.number().int().positive()),
  createdAt: z.number().int().positive(),
  updatedAt: z.number().int().positive(),
});

/**
 * KV Storage: Shared list data
 * Key pattern: share:{shareId}
 * TTL: 30 days
 */
export const KvSharedListDataSchema = z.object({
  shareId: z.string().length(8),
  userId: z.string().uuid(),
  locationIds: z.array(z.number().int().positive()),
  createdAt: z.number().int().positive(),
});

export type KvUserStarData = z.infer<typeof KvUserStarDataSchema>;
export type KvSharedListData = z.infer<typeof KvSharedListDataSchema>;
```

### File: `workers/api/src/schemas/api.schemas.ts`

```typescript
import { z } from 'zod';

/**
 * API Request: Create share
 * POST /api/share
 */
export const ApiCreateShareRequestSchema = z.object({
  userId: z.string().uuid(),
  locationIds: z.array(z.number().int().positive()).min(1).max(50),
});

/**
 * API Response: Create share
 * POST /api/share
 */
export const ApiCreateShareResponseSchema = z.object({
  shareId: z.string().length(8),
  url: z.string().url(),
  expiresAt: z.number().int().positive(),
});

/**
 * API Request: Star bulk
 * POST /api/users/:userId/starred/bulk
 */
export const ApiStarBulkRequestSchema = z.object({
  locationIds: z.array(z.number().int().positive()).min(1).max(50),
});

export type ApiCreateShareRequest = z.infer<typeof ApiCreateShareRequestSchema>;
export type ApiCreateShareResponse = z.infer<typeof ApiCreateShareResponseSchema>;
export type ApiStarBulkRequest = z.infer<typeof ApiStarBulkRequestSchema>;
```

---

## Complete File Structure

```
src/
├── schemas/
│   ├── api/                              # API layer (Client ↔ Worker)
│   │   ├── location.api.schema.ts        # Location API DTOs
│   │   │   ├── ApiGetLocationsResponse
│   │   │   ├── ApiCreateLocationRequest
│   │   │   ├── ApiCreateLocationResponse
│   │   │   ├── ApiUpdateLocationRequest
│   │   │   ├── ApiUpdateLocationResponse
│   │   │   └── ApiDeleteLocationResponse
│   │   ├── star.api.schema.ts            # Star API DTOs
│   │   │   ├── ApiGetStarredResponse
│   │   │   ├── ApiToggleStarResponse
│   │   │   ├── ApiStarBulkRequest
│   │   │   └── ApiStarBulkResponse
│   │   └── share.api.schema.ts           # Share API DTOs
│   │       ├── ApiCreateShareRequest
│   │       ├── ApiCreateShareResponse
│   │       └── ApiGetShareResponse
│   ├── kv/                               # KV storage layer (Worker)
│   │   ├── user.kv.schema.ts             # User KV DTOs
│   │   │   └── KvUserStarData
│   │   └── share.kv.schema.ts            # Share KV DTOs
│   │       └── KvSharedListData
│   ├── local/                            # localStorage layer (Client)
│   │   └── preferences.local.schema.ts   # Preferences DTO
│   │       └── LocalStorageUserPreferences
│   ├── domain/                           # Domain entities (Shared)
│   │   └── location.domain.schema.ts     # Core Location entity
│   │       └── LocationDomain
│   └── index.ts                          # Re-export all schemas
└── services/
    ├── locationService.ts                # Uses Api*Location* schemas
    ├── starService.ts                    # Uses Api*Star* schemas
    └── shareService.ts                   # Uses Api*Share* schemas

workers/api/src/
├── schemas/
│   ├── kv.schemas.ts                     # KV storage schemas
│   │   ├── KvUserStarData
│   │   └── KvSharedListData
│   └── api.schemas.ts                    # API request/response schemas
│       ├── ApiCreateShareRequest
│       ├── ApiCreateShareResponse
│       └── ApiStarBulkRequest
└── index.ts                              # Worker implementation
```

---

## Naming Patterns

### API Layer (Client ↔ Worker):

```typescript
// Requests (Client → Worker)
ApiCreateLocationRequest
ApiUpdateLocationRequest
ApiStarBulkRequest
ApiCreateShareRequest

// Responses (Worker → Client)
ApiGetLocationsResponse
ApiCreateLocationResponse
ApiToggleStarResponse
ApiGetShareResponse
```

### KV Layer (Worker Storage):

```typescript
// Storage DTOs
KvUserStarData          // Stored at: user:{userId}
KvSharedListData        // Stored at: share:{shareId}
KvLocationData          // Stored at: location:{locationId}
```

### localStorage Layer (Client Storage):

```typescript
// Client-only storage
LocalStorageUserPreferences  // Stored at: map-search-preferences
LocalStorageUserId           // Stored at: map-search-user-id
```

### Domain Layer (Shared):

```typescript
// Core entities used everywhere
LocationDomain
UserDomain
ShareDomain
```

---

## Benefits of This Naming Strategy

### ✅ Clear Service Layer:

```typescript
// ✅ Immediately clear this is an API response
type Response = ApiGetStarredResponse;

// ✅ Immediately clear this is stored in KV
type KvData = KvUserStarData;

// ✅ Immediately clear this is in localStorage
type LocalData = LocalStorageUserPreferences;
```

### ✅ Clear Direction:

```typescript
// ✅ Request (Client → Server)
ApiCreateLocationRequest

// ✅ Response (Server → Client)
ApiCreateLocationResponse
```

### ✅ Clear Purpose:

```typescript
// ✅ What operation?
ApiCreateShareRequest    // Creating a share
ApiGetStarredResponse    // Getting starred locations
ApiToggleStarResponse    // Toggling star status
```

### ✅ Prevents Confusion:

```typescript
// ❌ Ambiguous
LocationData          // Where? API? KV? localStorage?
ShareResponse         // From what? API? KV?

// ✅ Clear
ApiLocationResponse   // From API
KvLocationData        // From KV
LocalStorageLocation  // From localStorage
```

---

## Type Imports in Services

### Clear and Explicit:

```typescript
// starService.ts
import {
  ApiGetStarredResponse,
  ApiToggleStarResponse,
  ApiStarBulkRequest,
  ApiStarBulkResponse,
} from '../schemas/api/star.api.schema';

// Immediately clear these are API types
export async function fetchStarred(userId: string): Promise<ApiGetStarredResponse> {
  // ...
}
```

### Worker Implementation:

```typescript
// workers/api/src/index.ts
import { KvUserStarData, KvSharedListData } from './schemas/kv.schemas';
import { ApiCreateShareRequest, ApiCreateShareResponse } from './schemas/api.schemas';

// Clear what's stored in KV vs what's sent over API
const kvData: KvUserStarData = { ... };
const apiResponse: ApiCreateShareResponse = { ... };
```

---

## Schema Re-exports

### File: `src/schemas/index.ts`

```typescript
// Domain entities
export * from './domain/location.domain.schema';

// API layer
export * from './api/location.api.schema';
export * from './api/star.api.schema';
export * from './api/share.api.schema';

// KV layer (for Worker)
export * from './kv/user.kv.schema';
export * from './kv/share.kv.schema';

// localStorage layer
export * from './local/preferences.local.schema';
```

**Usage:**
```typescript
// Import from index for convenience
import {
  LocationDomain,
  ApiGetStarredResponse,
  KvUserStarData,
  LocalStorageUserPreferences,
} from '@schemas';
```

---

## Documentation in Code

### Add JSDoc Comments:

```typescript
/**
 * API Response: Get user's starred locations
 * 
 * Endpoint: GET /api/users/:userId/starred
 * Used by: starService.fetchStarredLocationIds()
 * 
 * @example
 * {
 *   userId: "550e8400-e29b-41d4-a716-446655440000",
 *   starredLocationIds: [1, 3, 5],
 *   updatedAt: 1703001234567
 * }
 */
export const ApiGetStarredResponseSchema = z.object({
  userId: z.string().uuid(),
  starredLocationIds: z.array(z.number().int().positive()),
  updatedAt: z.number().int().positive(),
});
```

---

## Summary

### ✅ Proper DTO Organization:

**Naming Pattern**: `{Service}{Entity}{Direction}{Purpose}`

**Service Layers**:
- `Api*` - API request/response
- `Kv*` - Cloudflare KV storage
- `LocalStorage*` - Browser localStorage
- `*Domain` - Core entities

**Direction**:
- `*Request` - Client → Server
- `*Response` - Server → Client
- `*Data` - Storage format

**Benefits**:
- ✅ Immediately clear where DTO is used
- ✅ Clear request vs response
- ✅ Clear storage layer
- ✅ Prevents confusion
- ✅ Self-documenting code
- ✅ Easy to navigate codebase

This naming strategy makes the codebase much more maintainable and understandable!