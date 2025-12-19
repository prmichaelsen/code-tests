# Map Component Design

## Overview
Full-page Google Maps component that displays location markers and handles map interactions. Uses `@react-google-maps/api` for React integration.

## Visual Design
- **Position**: Full viewport background
- **Size**: 100% width and height
- **Center**: Boston area (42.354022, -71.046245)
- **Zoom**: 12 (city level)
- **Style**: Default Google Maps style

## Props Interface
```typescript
interface MapProps {
  locations: Location[];
  selectedLocation: Location | null;
  onMarkerClick: (location: Location) => void;
  className?: string;
}
```

## State Management
- Uses `MapContext` for map instance, center, zoom
- Uses `LocationContext` for locations and selected location
- Local state for markers

## Behavior
1. **Initial Load**: Centers on Boston area
2. **Add Markers**: Creates markers for all locations
3. **Click Marker**: 
   - Opens LocationModal with location details
   - Highlights marker (different color/animation)
4. **Pan/Zoom**: Updates map center and zoom in context
5. **Search Result Click**: Pans to location and adds/highlights marker

## Google Maps Integration
```typescript
import { GoogleMap, Marker, useLoadScript } from '@react-google-maps/api';

const mapContainerStyle = {
  width: '100%',
  height: '100vh',
};

const center = {
  lat: 42.354022,
  lng: -71.046245,
};

const options = {
  disableDefaultUI: false,
  zoomControl: true,
  mapTypeControl: false,
  streetViewControl: false,
  fullscreenControl: false,
};
```

## Marker Management
```typescript
interface MarkerData {
  id: number;
  position: { lat: number; lng: number };
  title: string;
  icon?: string; // Custom marker icon
  animation?: google.maps.Animation;
}
```

## Custom Marker Icon
- Use `icon-pin.svg` for custom marker appearance
- Blue color (#4285F4) for normal markers
- Different color/animation for selected marker
- Scale: 32x32 pixels

## Styling
```css
.map-container {
  width: 100%;
  height: 100vh;
  position: relative;
}

.map-wrapper {
  width: 100%;
  height: 100%;
}

/* Custom marker styles via Google Maps API */
.custom-marker {
  width: 32px;
  height: 32px;
}
```

## Map Events
```typescript
// ✅ All event handlers properly wrapped with useCallback
const handleMapLoad = useCallback((map: google.maps.Map) => {
  setMapInstance(map);
}, [setMapInstance]); // From MapContext (stable)

const handleMarkerClick = useCallback((location: Location) => {
  setSelectedLocation(location);
  // Modal will open automatically via context
}, [setSelectedLocation]); // From LocationContext (stable)

const handleMapClick = useCallback(() => {
  // Optional: close modal when clicking map
  setSelectedLocation(null);
}, [setSelectedLocation]); // From LocationContext (stable)

const handleCenterChanged = useCallback(() => {
  if (mapInstance) {
    const newCenter = mapInstance.getCenter();
    if (newCenter) {
      setCenter({
        lat: newCenter.lat(),
        lng: newCenter.lng(),
      });
    }
  }
}, [mapInstance, setCenter]); // mapInstance from state, setCenter from context
```

## Marker Clustering (Optional Enhancement)
```typescript
import { MarkerClusterer } from '@react-google-maps/api';

// Cluster markers when zoomed out
<MarkerClusterer>
  {(clusterer) =>
    locations.map((location) => (
      <Marker
        key={location.id}
        position={{ lat: location.location.lat, lng: location.location.lon }}
        clusterer={clusterer}
        onClick={() => handleMarkerClick(location)}
      />
    ))
  }
</MarkerClusterer>
```

## Pan to Location
```typescript
// ✅ Wrapped with useCallback since it's called from other components
const panToLocation = useCallback((location: Location) => {
  if (mapInstance) {
    mapInstance.panTo({
      lat: location.location.lat,
      lng: location.location.lon,
    });
    mapInstance.setZoom(15); // Zoom in closer
  }
}, [mapInstance]); // Depends on mapInstance from state
```

## Accessibility
- `aria-label="Google Maps showing location markers"`
- Keyboard navigation for markers (Tab, Enter)
- Screen reader announcements for marker selection

## Performance Considerations
- Lazy load Google Maps API
- Memoize marker components
- Use marker clustering for many locations
- Debounce map events (center changed, zoom changed)

## Dependencies
- `@react-google-maps/api` for React integration
- `MapContext` for map state
- `LocationContext` for location data
- Google Maps API key from environment

## File Location
`src/components/Map/Map.tsx`
`src/components/Map/Map.module.css`
`src/components/Map/Marker.tsx` (optional separate component)

## Example Usage
```typescript
<GoogleMap
  mapContainerStyle={mapContainerStyle}
  center={center}
  zoom={zoom}
  options={options}
  onLoad={handleMapLoad}
  onClick={handleMapClick}
  onCenterChanged={handleCenterChanged}
>
  {locations.map((location) => (
    <Marker
      key={location.id}
      position={{
        lat: location.location.lat,
        lng: location.location.lon,
      }}
      title={location.name}
      onClick={() => handleMarkerClick(location)}
      icon={
        selectedLocation?.id === location.id
          ? selectedMarkerIcon
          : defaultMarkerIcon
      }
    />
  ))}
</GoogleMap>
```

## Error Handling
- Handle Google Maps API load failures
- Show error message if API key is invalid
- Fallback to static map image if Maps fails to load
- Handle network errors gracefully