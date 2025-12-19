# App Component Design

## Overview
The root application component that orchestrates all other components and provides the Google Maps API context.

## Component Hierarchy
```
App
├── LoadScript (Google Maps API)
│   ├── SearchBar
│   ├── SearchResults
│   ├── Map
│   │   └── Markers
│   └── LocationModal
```

## Props Interface
```typescript
// App is the root component, no props needed
interface AppProps {}
```

## Layout Structure
```typescript
<LoadScript googleMapsApiKey={GOOGLE_MAPS_API_KEY} libraries={libraries}>
  <div className="app">
    {/* Search UI - Fixed top-left */}
    <div className="search-container">
      <SearchBar />
      <SearchResults />
    </div>

    {/* Map - Full page background */}
    <Map />

    {/* Modal - Rendered via portal when open */}
    <LocationModal />
  </div>
</LoadScript>
```

## Styling
```css
.app {
  width: 100%;
  height: 100vh;
  position: relative;
  overflow: hidden;
}

.search-container {
  position: fixed;
  top: 20px;
  left: 20px;
  z-index: 1000;
  width: 400px;
}

/* Ensure map fills entire viewport */
.map-container {
  width: 100%;
  height: 100vh;
}
```

## Google Maps LoadScript Configuration
```typescript
const GOOGLE_MAPS_API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;

const libraries: ('places' | 'geometry')[] = ['places'];

const loadScriptOptions = {
  googleMapsApiKey: GOOGLE_MAPS_API_KEY,
  libraries,
  preventGoogleFontsLoading: false, // Set to true to prevent Google Fonts
};
```

## Context Providers
Already wrapped in `main.tsx`:
```typescript
<LocationProvider>
  <MapProvider>
    <SearchProvider>
      <App />
    </SearchProvider>
  </MapProvider>
</LocationProvider>
```

## Initial Data Loading
```typescript
const App: React.FC = () => {
  const { locations, setLocations } = useLocations();

  useEffect(() => {
    // Load initial locations from API or mock data
    const loadLocations = async () => {
      try {
        const data = await fetchLocations();
        setLocations(data);
      } catch (error) {
        console.error('Failed to load locations:', error);
        // Fallback to mock data
        setLocations(mockLocations);
      }
    };

    loadLocations();
  }, []);

  return (
    <LoadScript {...loadScriptOptions}>
      {/* App content */}
    </LoadScript>
  );
};
```

## Error Boundary (Optional)
```typescript
class ErrorBoundary extends React.Component<
  { children: ReactNode },
  { hasError: boolean }
> {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('App Error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-screen">
          <h1>Something went wrong</h1>
          <button onClick={() => window.location.reload()}>
            Reload Page
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

// Wrap App with ErrorBoundary in main.tsx
```

## Loading State
```typescript
const App: React.FC = () => {
  const [isLoading, setIsLoading] = useState(true);

  if (isLoading) {
    return (
      <div className="loading-screen">
        <div className="spinner" />
        <p>Loading map...</p>
      </div>
    );
  }

  return (
    <LoadScript
      {...loadScriptOptions}
      onLoad={() => setIsLoading(false)}
    >
      {/* App content */}
    </LoadScript>
  );
};
```

## Responsive Design
```css
@media (max-width: 768px) {
  .search-container {
    width: calc(100% - 40px);
    max-width: 400px;
  }
}

@media (max-width: 480px) {
  .search-container {
    top: 10px;
    left: 10px;
    right: 10px;
    width: auto;
  }
}
```

## Global Styles
```css
/* Reset and base styles */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html,
body,
#root {
  width: 100%;
  height: 100%;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto',
    'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans',
    'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Prevent body scroll when modal is open */
body.modal-open {
  overflow: hidden;
}
```

## Performance Optimizations
```typescript
// Lazy load components
const LocationModal = lazy(() => import('./components/Modal/LocationModal'));
const TrafficChart = lazy(() => import('./components/Chart/TrafficChart'));

// Memoize expensive components
const MemoizedMap = memo(Map);
const MemoizedSearchResults = memo(SearchResults);
```

## Environment Variables Usage
```typescript
const config = {
  googleMapsApiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY,
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL,
  isDevelopment: import.meta.env.DEV,
  isProduction: import.meta.env.PROD,
};

// Validate required env vars
if (!config.googleMapsApiKey) {
  throw new Error('VITE_GOOGLE_MAPS_API_KEY is required');
}
```

## File Location
`src/App.tsx`
`src/App.css`

## Dependencies
- `@react-google-maps/api` for LoadScript
- All context providers (from main.tsx)
- All child components (SearchBar, SearchResults, Map, LocationModal)

## Testing
```typescript
describe('App', () => {
  it('renders without crashing', () => {
    render(<App />);
  });

  it('loads Google Maps API', async () => {
    render(<App />);
    await waitFor(() => {
      expect(screen.getByRole('search')).toBeInTheDocument();
    });
  });

  it('displays search bar and map', () => {
    render(<App />);
    expect(screen.getByPlaceholderText('Search...')).toBeInTheDocument();
  });
});
```

## Complete App.tsx Example
```typescript
import React, { useEffect, useState } from 'react';
import { LoadScript } from '@react-google-maps/api';
import Map from './components/Map/Map';
import SearchBar from './components/Search/SearchBar';
import SearchResults from './components/Search/SearchResults';
import LocationModal from './components/Modal/LocationModal';
import { useLocations } from './contexts/LocationContext';
import { fetchLocations } from './services/locationService';
import { mockLocations } from './services/mockData';
import './App.css';

const GOOGLE_MAPS_API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;
const libraries: ('places' | 'geometry')[] = ['places'];

const App: React.FC = () => {
  const [isLoading, setIsLoading] = useState(true);
  const { setLocations } = useLocations();

  useEffect(() => {
    const loadInitialData = async () => {
      try {
        const data = await fetchLocations();
        setLocations(data);
      } catch (error) {
        console.error('Failed to load locations, using mock data:', error);
        setLocations(mockLocations);
      } finally {
        setIsLoading(false);
      }
    };

    loadInitialData();
  }, [setLocations]);

  if (isLoading) {
    return (
      <div className="loading-screen">
        <div className="spinner" />
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <LoadScript
      googleMapsApiKey={GOOGLE_MAPS_API_KEY}
      libraries={libraries}
    >
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