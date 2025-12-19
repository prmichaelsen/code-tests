# Front-End Bootstrap Plan: TypeScript + Vite + React + React Context

## Project Overview
Bootstrap a modern React application using TypeScript, Vite, and React Context for state management to build the map search interface.

---

## Technology Stack

### Core Technologies
- **TypeScript** - Type-safe JavaScript with enhanced IDE support
- **Vite** - Fast build tool and dev server
- **React 18+** - UI library with hooks
- **React Context API** - Global state management (alternative to Redux)

### Additional Libraries
- **@react-google-maps/api** - React wrapper for Google Maps
- **Chart.js + react-chartjs-2** - Data visualization
- **Native Fetch API** - HTTP client (built-in, no installation needed)
- **React Router** (optional) - Client-side routing

---

## Phase 1: Project Initialization

### Step 1.1: Create Vite + React + TypeScript Project

```bash
# Navigate to front-end directory
cd front-end

# Create new Vite project with React + TypeScript template
npm create vite@latest map-search-app -- --template react-ts

# Navigate into project
cd map-search-app

# Install dependencies
npm install
```

**Expected Output:**
```
map-search-app/
├── node_modules/
├── public/
├── src/
│   ├── assets/
│   ├── App.css
│   ├── App.tsx
│   ├── index.css
│   ├── main.tsx
│   └── vite-env.d.ts
├── .gitignore
├── index.html
├── package.json
├── tsconfig.json
├── tsconfig.node.json
└── vite.config.ts
```

### Step 1.2: Install Required Dependencies

```bash
# Google Maps React wrapper
npm install @react-google-maps/api

# Chart.js for data visualization
npm install chart.js react-chartjs-2

# Type definitions
npm install -D @types/google.maps

# Note: We'll use native Fetch API (built-in) instead of axios
```

### Step 1.3: Install Development Dependencies

```bash
# ESLint for TypeScript
npm install -D @typescript-eslint/eslint-plugin @typescript-eslint/parser

# Prettier for code formatting
npm install -D prettier eslint-config-prettier eslint-plugin-prettier

# Additional type safety
npm install -D @types/node
```

---

## Phase 2: Project Structure Setup

### Step 2.1: Create Directory Structure

```bash
# Create directories
mkdir -p src/{components,contexts,hooks,services,types,utils,assets}
mkdir -p src/components/{Map,Search,Modal,Chart}
```

**Final Structure:**
```
src/
├── assets/              # Static assets (SVG icons, images)
│   ├── icon-pin.svg
│   └── icon-search.svg
├── components/          # React components
│   ├── Map/
│   │   ├── Map.tsx
│   │   ├── Marker.tsx
│   │   └── Map.module.css
│   ├── Search/
│   │   ├── SearchBar.tsx
│   │   ├── SearchResults.tsx
│   │   └── Search.module.css
│   ├── Modal/
│   │   ├── LocationModal.tsx
│   │   └── Modal.module.css
│   └── Chart/
│       ├── TrafficChart.tsx
│       └── Chart.module.css
├── contexts/            # React Context providers
│   ├── LocationContext.tsx
│   ├── SearchContext.tsx
│   └── MapContext.tsx
├── hooks/               # Custom React hooks
│   ├── useGoogleMaps.ts
│   ├── useSearch.ts
│   └── useLocations.ts
├── services/            # API services
│   ├── api.ts
│   ├── locationService.ts
│   └── mockData.ts
├── types/               # TypeScript type definitions
│   ├── location.types.ts
│   ├── search.types.ts
│   └── map.types.ts
├── utils/               # Utility functions
│   ├── searchUtils.ts
│   └── mapUtils.ts
├── App.tsx              # Main App component
├── main.tsx             # Entry point
└── vite-env.d.ts        # Vite type definitions
```

### Step 2.2: Copy Assets

```bash
# Copy SVG icons from original project
cp ../map-search-test/icon-pin.svg src/assets/
cp ../map-search-test/icon-search.svg src/assets/

# Copy sample data
cp ../map-search-test/sample-data.js src/services/mockData.ts
```

---

## Phase 3: TypeScript Type Definitions

### Step 3.1: Create Core Type Definitions

**File: `src/types/location.types.ts`**
```typescript
export interface Location {
  id: string;
  name: string;
  lat: number;
  lng: number;
  address?: string;
  description?: string;
  category?: string;
  avgStoreTraffic?: number[];
  images?: string[];
  link?: string;
  starred?: boolean;
}

export interface LocationState {
  locations: Location[];
  selectedLocation: Location | null;
  starredLocations: Location[];
}

export interface LocationContextType extends LocationState {
  setSelectedLocation: (location: Location | null) => void;
  toggleStar: (locationId: string) => void;
  addLocation: (location: Omit<Location, 'id'>) => Promise<void>;
  updateLocation: (id: string, location: Partial<Location>) => Promise<void>;
  deleteLocation: (id: string) => Promise<void>;
}
```

**File: `src/types/search.types.ts`**
```typescript
export interface SearchState {
  query: string;
  results: Location[];
  isSearching: boolean;
}

export interface SearchContextType extends SearchState {
  setQuery: (query: string) => void;
  clearSearch: () => void;
}
```

**File: `src/types/map.types.ts`**
```typescript
export interface MapState {
  center: google.maps.LatLngLiteral;
  zoom: number;
  mapInstance: google.maps.Map | null;
}

export interface MapContextType extends MapState {
  setCenter: (center: google.maps.LatLngLiteral) => void;
  setZoom: (zoom: number) => void;
  setMapInstance: (map: google.maps.Map | null) => void;
  panTo: (location: google.maps.LatLngLiteral) => void;
}
```

---

## Phase 4: Environment Configuration

### Step 4.1: Create Environment Files

**File: `.env`**
```env
VITE_GOOGLE_MAPS_API_KEY=your_api_key_here
VITE_API_BASE_URL=http://localhost:3001
```

**File: `.env.example`**
```env
VITE_GOOGLE_MAPS_API_KEY=your_google_maps_api_key
VITE_API_BASE_URL=http://localhost:3001
```

### Step 4.2: Update .gitignore

```gitignore
# Environment variables
.env
.env.local
.env.*.local

# Dependencies
node_modules

# Build output
dist
dist-ssr
*.local

# Editor
.vscode/*
!.vscode/extensions.json
.idea
.DS_Store
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?
```

### Step 4.3: Create Environment Type Definitions

**File: `src/vite-env.d.ts`** (update existing)
```typescript
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_GOOGLE_MAPS_API_KEY: string;
  readonly VITE_API_BASE_URL: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
```

---

## Phase 5: React Context Setup

### Step 5.1: Create Location Context

**File: `src/contexts/LocationContext.tsx`**
```typescript
import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { Location, LocationContextType, LocationState } from '../types/location.types';
import * as locationService from '../services/locationService';

const LocationContext = createContext<LocationContextType | undefined>(undefined);

export const LocationProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, setState] = useState<LocationState>({
    locations: [],
    selectedLocation: null,
    starredLocations: [],
  });

  const setSelectedLocation = useCallback((location: Location | null) => {
    setState(prev => ({ ...prev, selectedLocation: location }));
  }, []);

  const toggleStar = useCallback((locationId: string) => {
    setState(prev => {
      const location = prev.locations.find(loc => loc.id === locationId);
      if (!location) return prev;

      const isStarred = prev.starredLocations.some(loc => loc.id === locationId);
      const starredLocations = isStarred
        ? prev.starredLocations.filter(loc => loc.id !== locationId)
        : [...prev.starredLocations, location];

      return { ...prev, starredLocations };
    });
  }, []);

  const addLocation = useCallback(async (location: Omit<Location, 'id'>) => {
    const newLocation = await locationService.createLocation(location);
    setState(prev => ({
      ...prev,
      locations: [...prev.locations, newLocation],
    }));
  }, []);

  const updateLocation = useCallback(async (id: string, updates: Partial<Location>) => {
    const updated = await locationService.updateLocation(id, updates);
    setState(prev => ({
      ...prev,
      locations: prev.locations.map(loc => loc.id === id ? updated : loc),
    }));
  }, []);

  const deleteLocation = useCallback(async (id: string) => {
    await locationService.deleteLocation(id);
    setState(prev => ({
      ...prev,
      locations: prev.locations.filter(loc => loc.id !== id),
      starredLocations: prev.starredLocations.filter(loc => loc.id !== id),
    }));
  }, []);

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

### Step 5.2: Create Search Context

**File: `src/contexts/SearchContext.tsx`**
```typescript
import React, { createContext, useContext, useState, useCallback, ReactNode, useEffect } from 'react';
import { SearchContextType, SearchState } from '../types/search.types';
import { Location } from '../types/location.types';
import { useLocations } from './LocationContext';
import { searchLocations } from '../utils/searchUtils';

const SearchContext = createContext<SearchContextType | undefined>(undefined);

export const SearchProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const { locations } = useLocations();
  const [state, setState] = useState<SearchState>({
    query: '',
    results: [],
    isSearching: false,
  });

  const setQuery = useCallback((query: string) => {
    setState(prev => ({ ...prev, query, isSearching: true }));
  }, []);

  const clearSearch = useCallback(() => {
    setState({ query: '', results: [], isSearching: false });
  }, []);

  // Perform search when query changes
  useEffect(() => {
    if (!state.query.trim()) {
      setState(prev => ({ ...prev, results: [], isSearching: false }));
      return;
    }

    const timeoutId = setTimeout(() => {
      const results = searchLocations(locations, state.query);
      setState(prev => ({ ...prev, results, isSearching: false }));
    }, 300); // Debounce search

    return () => clearTimeout(timeoutId);
  }, [state.query, locations]);

  const value: SearchContextType = {
    ...state,
    setQuery,
    clearSearch,
  };

  return <SearchContext.Provider value={value}>{children}</SearchContext.Provider>;
};

export const useSearch = (): SearchContextType => {
  const context = useContext(SearchContext);
  if (!context) {
    throw new Error('useSearch must be used within SearchProvider');
  }
  return context;
};
```

### Step 5.3: Create Map Context

**File: `src/contexts/MapContext.tsx`**
```typescript
import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { MapContextType, MapState } from '../types/map.types';

const DEFAULT_CENTER = { lat: 37.7749, lng: -122.4194 }; // San Francisco
const DEFAULT_ZOOM = 12;

const MapContext = createContext<MapContextType | undefined>(undefined);

export const MapProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, setState] = useState<MapState>({
    center: DEFAULT_CENTER,
    zoom: DEFAULT_ZOOM,
    mapInstance: null,
  });

  const setCenter = useCallback((center: google.maps.LatLngLiteral) => {
    setState(prev => ({ ...prev, center }));
  }, []);

  const setZoom = useCallback((zoom: number) => {
    setState(prev => ({ ...prev, zoom }));
  }, []);

  const setMapInstance = useCallback((map: google.maps.Map | null) => {
    setState(prev => ({ ...prev, mapInstance: map }));
  }, []);

  const panTo = useCallback((location: google.maps.LatLngLiteral) => {
    if (state.mapInstance) {
      state.mapInstance.panTo(location);
      state.mapInstance.setZoom(15);
    }
    setCenter(location);
  }, [state.mapInstance, setCenter]);

  const value: MapContextType = {
    ...state,
    setCenter,
    setZoom,
    setMapInstance,
    panTo,
  };

  return <MapContext.Provider value={value}>{children}</MapContext.Provider>;
};

export const useMap = (): MapContextType => {
  const context = useContext(MapContext);
  if (!context) {
    throw new Error('useMap must be used within MapProvider');
  }
  return context;
};
```

---

## Phase 6: Service Layer Setup

### Step 6.1: Create API Client

**File: `src/services/api.ts`**
```typescript
import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3001';

export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if needed
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);
```

### Step 6.2: Create Location Service

**File: `src/services/locationService.ts`**
```typescript
import { apiClient } from './api';
import { Location } from '../types/location.types';

const ENDPOINTS = {
  LOCATIONS: '/locations',
};

export const fetchLocations = async (): Promise<Location[]> => {
  const response = await apiClient.get<Location[]>(ENDPOINTS.LOCATIONS);
  return response.data;
};

export const createLocation = async (location: Omit<Location, 'id'>): Promise<Location> => {
  const response = await apiClient.post<Location>(ENDPOINTS.LOCATIONS, location);
  return response.data;
};

export const updateLocation = async (id: string, updates: Partial<Location>): Promise<Location> => {
  const response = await apiClient.put<Location>(`${ENDPOINTS.LOCATIONS}/${id}`, updates);
  return response.data;
};

export const deleteLocation = async (id: string): Promise<void> => {
  await apiClient.delete(`${ENDPOINTS.LOCATIONS}/${id}`);
};
```

### Step 6.3: Convert Mock Data to TypeScript

**File: `src/services/mockData.ts`**
```typescript
import { Location } from '../types/location.types';

export const mockLocations: Location[] = [
  {
    id: '1',
    name: 'Sample Location 1',
    lat: 37.7749,
    lng: -122.4194,
    address: '123 Main St, San Francisco, CA',
    description: 'A great location',
    category: 'Restaurant',
    avgStoreTraffic: [120, 150, 180, 200, 190, 160, 140],
    starred: false,
  },
  // Add more mock data from sample-data.js
];
```

---

## Phase 7: Utility Functions

### Step 7.1: Create Search Utilities

**File: `src/utils/searchUtils.ts`**
```typescript
import { Location } from '../types/location.types';

export const searchLocations = (locations: Location[], query: string): Location[] => {
  const lowerQuery = query.toLowerCase().trim();
  
  if (!lowerQuery) return [];

  return locations.filter(location => 
    location.name.toLowerCase().includes(lowerQuery) ||
    location.address?.toLowerCase().includes(lowerQuery) ||
    location.category?.toLowerCase().includes(lowerQuery)
  );
};

export const highlightMatch = (text: string, query: string): string => {
  if (!query) return text;
  
  const regex = new RegExp(`(${query})`, 'gi');
  return text.replace(regex, '<mark>$1</mark>');
};
```

---

## Phase 8: Configuration Files

### Step 8.1: Update TypeScript Config

**File: `tsconfig.json`** (update)
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@contexts/*": ["src/contexts/*"],
      "@hooks/*": ["src/hooks/*"],
      "@services/*": ["src/services/*"],
      "@types/*": ["src/types/*"],
      "@utils/*": ["src/utils/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### Step 8.2: Update Vite Config

**File: `vite.config.ts`** (update)
```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@contexts': path.resolve(__dirname, './src/contexts'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
      '@services': path.resolve(__dirname, './src/services'),
      '@types': path.resolve(__dirname, './src/types'),
      '@utils': path.resolve(__dirname, './src/utils'),
    },
  },
  server: {
    port: 3000,
    open: true,
  },
});
```

### Step 8.3: Create ESLint Config

**File: `.eslintrc.cjs`**
```javascript
module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
    'prettier',
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs'],
  parser: '@typescript-eslint/parser',
  plugins: ['react-refresh'],
  rules: {
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
  },
};
```

### Step 8.4: Create Prettier Config

**File: `.prettierrc`**
```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false
}
```

---

## Phase 9: Main App Setup

### Step 9.1: Update Main Entry Point

**File: `src/main.tsx`**
```typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { LocationProvider } from './contexts/LocationContext';
import { SearchProvider } from './contexts/SearchContext';
import { MapProvider } from './contexts/MapContext';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <LocationProvider>
      <MapProvider>
        <SearchProvider>
          <App />
        </SearchProvider>
      </MapProvider>
    </LocationProvider>
  </React.StrictMode>
);
```

### Step 9.2: Create App Component

**File: `src/App.tsx`**
```typescript
import React from 'react';
import { LoadScript } from '@react-google-maps/api';
import Map from './components/Map/Map';
import SearchBar from './components/Search/SearchBar';
import SearchResults from './components/Search/SearchResults';
import LocationModal from './components/Modal/LocationModal';
import './App.css';

const GOOGLE_MAPS_API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;
const libraries: ('places' | 'geometry')[] = ['places'];

const App: React.FC = () => {
  return (
    <LoadScript googleMapsApiKey={GOOGLE_MAPS_API_KEY} libraries={libraries}>
      <div className="app">
        <div className="search-container">
          <SearchBar />
          <SearchResults />
        </div>
        <Map />
        <LocationModal />
      </div>
    </LoadScript>
  );
};

export default App;
```

---

## Phase 10: Package Scripts

### Step 10.1: Update package.json Scripts

**File: `package.json`** (add/update scripts)
```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "lint:fix": "eslint . --ext ts,tsx --fix",
    "format": "prettier --write \"src/**/*.{ts,tsx,css}\"",
    "preview": "vite preview",
    "type-check": "tsc --noEmit"
  }
}
```

---

## Phase 11: Mock API Server Setup

### Option A: JSON Server

**File: `db.json`** (in project root)
```json
{
  "locations": [
    {
      "id": "1",
      "name": "Sample Location",
      "lat": 37.7749,
      "lng": -122.4194,
      "address": "123 Main St",
      "description": "A great place",
      "category": "Restaurant",
      "avgStoreTraffic": [120, 150, 180, 200, 190, 160, 140],
      "starred": false
    }
  ]
}
```

**Add script to package.json:**
```json
{
  "scripts": {
    "api": "json-server --watch db.json --port 3001",
    "dev:full": "npm run api & npm run dev"
  }
}
```

---

## Phase 12: Development Workflow

### Step 12.1: Initial Development Commands

```bash
# Install all dependencies
npm install

# Start development server
npm run dev

# In another terminal, start mock API
npm run api

# Or run both together
npm run dev:full

# Type checking
npm run type-check

# Linting
npm run lint

# Format code
npm run format
```

### Step 12.2: Build for Production

```bash
# Build production bundle
npm run build

# Preview production build
npm run preview
```

---

## Implementation Order

### Week 1: Foundation
1. ✅ Initialize Vite + React + TypeScript project
2. ✅ Set up project structure
3. ✅ Create type definitions
4. ✅ Set up environment configuration
5. ✅ Create React Context providers
6. ✅ Set up service layer

### Week 2: Core Features
7. Create Map component with Google Maps
8. Create SearchBar component
9. Create SearchResults component
10. Implement search functionality
11. Add marker functionality

### Week 3: Advanced Features
12. Create LocationModal component
13. Implement star/favorite functionality
14. Add Chart component for traffic data
15. Implement CRUD operations
16. Add error handling and loading states

### Week 4: Polish & Testing
17. Add CSS modules and styling
18. Implement responsive design
19. Add unit tests
20. Performance optimization
21. Documentation

---

## Success Criteria

- [ ] TypeScript compiles without errors
- [ ] All ESLint rules pass
- [ ] Development server runs smoothly
- [ ] Hot module replacement works
- [ ] Type safety enforced throughout
- [ ] React Context properly manages state
- [ ] Google Maps integrates successfully
- [ ] Search functionality works in real-time
- [ ] CRUD operations functional
- [ ] Code is well-organized and maintainable

---

## Benefits of This Stack

### TypeScript
- ✅ Type safety catches errors at compile time
- ✅ Better IDE autocomplete and IntelliSense
- ✅ Self-documenting code through types
- ✅ Easier refactoring

### Vite
- ✅ Lightning-fast HMR (Hot Module Replacement)
- ✅ Optimized production builds
- ✅ Native ES modules support
- ✅ Better developer experience

### React Context
- ✅ No external state management library needed
- ✅ Built-in to React
- ✅ Simple and straightforward
- ✅ Perfect for medium-sized applications
- ✅ Easy to test

---

## Next Steps

1. Follow Phase 1 to initialize the project
2. Set up environment variables with Google Maps API key
3. Implement contexts one by one
4. Build components incrementally
5. Test each feature as you build
6. Refer to [`tasks.md`](./tasks.md) for detailed implementation tasks

---

## Resources

- [Vite Documentation](https://vitejs.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)
- [React Context API](https://react.dev/reference/react/createContext)
- [@react-google-maps/api](https://react-google-maps-api-docs.netlify.app/)