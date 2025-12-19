# Component Architecture Overview

## Core Components

We need **5 core components** to rebuild the map search application:

### 1. [App](./App.md) - Root Component
**Purpose**: Orchestrates all components and provides Google Maps API context

**Key Responsibilities**:
- Load Google Maps API via LoadScript
- Initialize application state
- Render component hierarchy
- Handle initial data loading

**File**: `src/App.tsx`

---

### 2. [SearchBar](./SearchBar.md) - Search Input
**Purpose**: Allows users to search for locations by name

**Key Responsibilities**:
- Accept user input
- Update search query in context
- Display search icon
- Handle focus/blur states
- Debounce search input

**File**: `src/components/Search/SearchBar.tsx`

---

### 3. [SearchResults](./SearchResults.md) - Results Dropdown
**Purpose**: Display filtered search results in a dropdown list

**Key Responsibilities**:
- Show matching locations
- Display result count
- Handle result selection
- Show "no results" message
- Keyboard navigation

**File**: `src/components/Search/SearchResults.tsx`

---

### 4. [Map](./Map.md) - Google Maps Display
**Purpose**: Full-page map with location markers

**Key Responsibilities**:
- Render Google Maps
- Display location markers
- Handle marker clicks
- Pan/zoom to locations
- Manage map instance

**File**: `src/components/Map/Map.tsx`

---

### 5. [LocationModal](./LocationModal.md) - Details Modal
**Purpose**: Show detailed location information in a centered modal

**Key Responsibilities**:
- Display location details
- Show images gallery
- Render traffic chart (if data available)
- Handle close actions
- Portal rendering

**File**: `src/components/Modal/LocationModal.tsx`

---

## Optional/Extra Credit Component

### 6. [TrafficChart](./TrafficChart.md) - Chart.js Visualization
**Purpose**: Visualize average store traffic by day of week

**Key Responsibilities**:
- Render bar chart
- Transform traffic data
- Handle null values
- Display tooltips

**File**: `src/components/Chart/TrafficChart.tsx`

---

## Component Communication Flow

```
User Types in SearchBar
  ↓
SearchContext updates query
  ↓
SearchResults filters and displays matches
  ↓
User clicks result
  ↓
LocationContext sets selected location
MapContext pans to location
  ↓
Map adds/highlights marker
  ↓
User clicks marker
  ↓
LocationContext sets selected location
  ↓
LocationModal opens with details
  ↓
(Optional) TrafficChart renders if data exists
```

## State Management

### LocationContext
- Manages all locations
- Tracks selected location
- Handles starred locations
- CRUD operations

### SearchContext
- Manages search query
- Filters results
- Debounces search

### MapContext
- Manages map instance
- Tracks center and zoom
- Handles pan/zoom operations

## Data Flow

```
API/Mock Data
  ↓
LocationContext (locations array)
  ↓
SearchContext (filters locations)
  ↓
SearchResults (displays filtered)
  ↓
Map (displays all as markers)
  ↓
LocationModal (displays selected)
```

## File Structure

```
src/
├── components/
│   ├── Search/
│   │   ├── SearchBar.tsx
│   │   ├── SearchBar.module.css
│   │   ├── SearchResults.tsx
│   │   └── SearchResults.module.css
│   ├── Map/
│   │   ├── Map.tsx
│   │   └── Map.module.css
│   ├── Modal/
│   │   ├── LocationModal.tsx
│   │   └── LocationModal.module.css
│   └── Chart/
│       ├── TrafficChart.tsx
│       └── TrafficChart.module.css
├── contexts/
│   ├── LocationContext.tsx
│   ├── SearchContext.tsx
│   └── MapContext.tsx
├── types/
│   ├── location.types.ts
│   ├── search.types.ts
│   └── map.types.ts
├── services/
│   ├── api.ts
│   ├── locationService.ts
│   └── mockData.ts
├── utils/
│   └── searchUtils.ts
├── assets/
│   ├── icon-pin.svg
│   └── icon-search.svg
├── App.tsx
├── App.css
└── main.tsx
```

## Implementation Order

### Phase 1: Foundation (Week 1)
1. ✅ Set up project structure
2. ✅ Create type definitions
3. ✅ Implement contexts
4. ✅ Set up service layer

### Phase 2: Core UI (Week 2)
5. **SearchBar** - Start here (simplest component)
6. **SearchResults** - Depends on SearchBar
7. **Map** - Independent, can be built in parallel
8. **LocationModal** - Depends on Map for trigger

### Phase 3: Enhancement (Week 3)
9. **TrafficChart** - Extra credit feature
10. **Styling** - Match design mockups
11. **Animations** - Smooth transitions
12. **Responsive** - Mobile optimization

## Component Dependencies

```
App (root)
├── SearchBar (independent)
├── SearchResults (depends on SearchBar)
├── Map (independent)
│   └── Markers (inline)
└── LocationModal (depends on Map)
    └── TrafficChart (optional, depends on data)
```

## Testing Strategy

### Unit Tests
- Test each component in isolation
- Mock context providers
- Test user interactions
- Verify accessibility

### Integration Tests
- Test component communication
- Test context updates
- Test API calls
- Test error handling

### E2E Tests (Optional)
- Test complete user flows
- Search → Select → View Modal
- Add/Edit/Delete locations

## Design Specifications Summary

### Colors
- **Primary Blue**: #4285F4 (Google Maps blue)
- **Dark Blue**: #3367D6 (hover states)
- **White**: #FFFFFF (backgrounds)
- **Gray Text**: #666666, #999999 (secondary text)
- **Dark Text**: #333333, #111827 (primary text)
- **Border**: #e5e7eb, #f0f0f0 (dividers)

### Typography
- **Font Family**: System fonts (-apple-system, BlinkMacSystemFont, etc.)
- **Search Input**: 16px
- **Result Name**: 16px, font-weight: 500
- **Coordinates**: 12px
- **Modal Title**: 20px, font-weight: 600
- **Description**: 16px, line-height: 1.6

### Spacing
- **Search Bar**: 20px from edges
- **Padding**: 12-24px (varies by component)
- **Border Radius**: 6-8px
- **Gaps**: 12px (standard spacing)

### Shadows
- **Search Bar**: `0 2px 8px rgba(0, 0, 0, 0.15)`
- **Modal**: `0 20px 25px -5px rgba(0, 0, 0, 0.1)`
- **Results**: `0 4px 12px rgba(0, 0, 0, 0.15)`

## Accessibility Checklist

- [ ] All interactive elements keyboard accessible
- [ ] Proper ARIA labels and roles
- [ ] Focus management in modal
- [ ] Color contrast meets WCAG AA
- [ ] Screen reader announcements
- [ ] Skip links for keyboard users
- [ ] Alt text for images

## Browser Support

- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions
- Mobile browsers: iOS Safari, Chrome Android

## Next Steps

1. Review each component design document
2. Start implementation with SearchBar (simplest)
3. Build SearchResults next
4. Implement Map component
5. Create LocationModal
6. Add TrafficChart (extra credit)
7. Style to match mockups
8. Test and refine

Each component design document includes:
- Visual specifications
- Props interface
- State management
- Behavior details
- Complete styling
- Accessibility requirements
- Dependencies
- Testing considerations