# SearchResults Component Design

## Overview
A dropdown list that displays filtered location results based on the search query. Appears below the SearchBar when there are results.

## Visual Design
- **Position**: Directly below SearchBar (fixed positioning)
- **Size**: Same width as SearchBar (~400px), variable height
- **Style**: White background, rounded bottom corners, shadow
- **Header**: Blue background with white text "Found X Result(s):"
- **Items**: White background with hover effect

## Props Interface
```typescript
interface SearchResultsProps {
  results: Location[];
  onSelectLocation: (location: Location) => void;
  isVisible: boolean;
  className?: string;
}
```

## State Management
- Receives results from `SearchContext`
- Uses `LocationContext` to set selected location
- Uses `MapContext` to pan map to location

## Behavior
1. **Display**: Shows when search query exists and has results
2. **Click Item**: 
   - Sets selected location in context
   - Pans map to location coordinates
   - Closes results dropdown
   - Adds marker to map
3. **No Results**: Shows "No locations found" message
4. **Hover**: Highlights result item
5. **Keyboard**: Arrow keys to navigate, Enter to select

## Data Structure
```typescript
interface Location {
  id: number;
  name: string;
  location: {
    lat: number;
    lon: number;
  };
  details?: {
    description?: string;
    website?: string;
  };
  images?: string[];
}
```

## Styling
```css
.search-results {
  position: fixed;
  top: 80px; /* Below search bar */
  left: 20px;
  width: 400px;
  z-index: 999;
  background: white;
  border-radius: 0 0 8px 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  max-height: 400px;
  overflow-y: auto;
}

.results-header {
  background: #4285F4;
  color: white;
  padding: 12px 16px;
  font-weight: 500;
  font-size: 14px;
}

.result-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  cursor: pointer;
  border-bottom: 1px solid #f0f0f0;
  transition: background 0.2s;
}

.result-item:hover {
  background: #f8f9fa;
}

.result-item:last-child {
  border-bottom: none;
}

.result-icon {
  width: 24px;
  height: 24px;
  margin-right: 12px;
  color: #4285F4;
}

.result-info {
  flex: 1;
}

.result-name {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  margin-bottom: 4px;
}

.result-coordinates {
  font-size: 12px;
  color: #666;
}

.no-results {
  padding: 16px;
  text-align: center;
  color: #666;
  font-size: 14px;
}
```

## Result Item Structure
```
┌─────────────────────────────────────┐
│ Found 1 Result:                     │ ← Blue header
├─────────────────────────────────────┤
│ 📍 Alberts Bike Shop                │ ← Result item
│    42.354022, -71.046245            │
└─────────────────────────────────────┘
```

## Accessibility
- `role="listbox"`
- `aria-label="Search results"`
- Each item has `role="option"`
- `aria-selected` for keyboard navigation
- `aria-live="polite"` for result count updates

## Interactions
1. **Click Result**:
   ```typescript
   // ✅ Properly wrapped with useCallback
   const handleSelectLocation = useCallback((location: Location) => {
     setSelectedLocation(location);
     panTo({ lat: location.location.lat, lng: location.location.lon });
     clearSearch(); // Optional: close results
   }, [setSelectedLocation, panTo, clearSearch]); // All from context (stable)
   ```

2. **Keyboard Navigation**:
   - Arrow Up/Down: Navigate results
   - Enter: Select highlighted result
   - Escape: Close results

## Dependencies
- `SearchContext` for results data
- `LocationContext` for setting selected location
- `MapContext` for panning map
- `icon-pin.svg` for location icon

## File Location
`src/components/Search/SearchResults.tsx`
`src/components/Search/SearchResults.module.css`