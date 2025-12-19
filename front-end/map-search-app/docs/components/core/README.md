# Core Reusable Components

## Overview
Reusable UI components that support the main application logic components. These are generic, composable building blocks that can be used throughout the app.

---

## Identified Core Components

### 1. Button Component
**Purpose**: Consistent button styling and behavior across the app

**Used in:**
- Visit Website button (LocationModal)
- Close button (LocationModal)
- Star button (LocationModal)
- Share button (App)
- Clear search button (SearchBar)

**Design**: [`Button.md`](./Button.md)

---

### 2. Icon Component
**Purpose**: SVG icon wrapper with consistent sizing and styling

**Used in:**
- Search icon (SearchBar)
- Location pin icon (SearchResults, LocationModal)
- Close icon (LocationModal)
- Star icon (StarButton)

**Design**: [`Icon.md`](./Icon.md)

---

### 3. LoadingSpinner Component
**Purpose**: Loading indicator for async operations

**Used in:**
- Initial app load
- Location data fetching
- Map loading
- API operations

**Design**: [`LoadingSpinner.md`](./LoadingSpinner.md)

---

### 4. ErrorBoundary Component
**Purpose**: Catch and display React errors gracefully

**Used in:**
- Wrap entire app
- Wrap individual components
- Prevent app crashes

**Design**: [`ErrorBoundary.md`](./ErrorBoundary.md)

---

### 5. Portal Component
**Purpose**: Render content outside React tree (for modals, tooltips)

**Used in:**
- LocationModal
- Tooltips
- Notifications

**Design**: [`Portal.md`](./Portal.md)

---

### 6. Card Component
**Purpose**: Consistent card/panel styling

**Used in:**
- Modal content wrapper
- Result items (alternative design)
- Location cards (if adding grid view)

**Design**: [`Card.md`](./Card.md)

---

### 7. Input Component
**Purpose**: Styled input field with consistent behavior

**Used in:**
- Search input (SearchBar)
- Location form fields (Add/Edit)
- Filter inputs

**Design**: [`Input.md`](./Input.md)

---

### 8. Tooltip Component
**Purpose**: Show additional information on hover

**Used in:**
- Map markers (show name on hover)
- Truncated text (show full text)
- Icon buttons (explain functionality)

**Design**: [`Tooltip.md`](./Tooltip.md)

---

## Component Hierarchy

```
Core Components (Reusable)
├── Button
│   ├── Primary variant
│   ├── Secondary variant
│   ├── Icon button variant
│   └── Link button variant
├── Icon
│   ├── Search
│   ├── Pin
│   ├── Star
│   ├── Close
│   └── Share
├── LoadingSpinner
├── ErrorBoundary
├── Portal
├── Card
├── Input
│   ├── Text input
│   ├── Search input
│   └── Textarea
└── Tooltip

Application Components (Business Logic)
├── App
├── SearchBar (uses: Input, Icon)
├── SearchResults (uses: Card, Icon)
├── Map
├── LocationModal (uses: Portal, Button, Icon, Card)
└── TrafficChart
```

---

## Benefits of Core Components

### ✅ Consistency
- Same look and feel across app
- Centralized styling
- Easier to maintain design system

### ✅ Reusability
- Write once, use everywhere
- Reduce code duplication
- Faster development

### ✅ Maintainability
- Single source of truth
- Easy to update globally
- Easier to test

### ✅ Accessibility
- Implement once, accessible everywhere
- Consistent keyboard navigation
- ARIA attributes built-in

### ✅ Type Safety
- Shared TypeScript interfaces
- Compile-time error checking
- Better IDE support

---

## Implementation Priority

### Phase 1: Essential (Build First)
1. **Icon** - Used everywhere
2. **Button** - Used in multiple places
3. **LoadingSpinner** - Needed for initial load

### Phase 2: Important (Build Next)
4. **Input** - Required for search
5. **ErrorBoundary** - Catch errors

### Phase 3: Nice to Have (Build Later)
6. **Card** - Improves consistency
7. **Tooltip** - Enhances UX

---

## File Structure

```
src/components/
├── core/                    # Reusable core components
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.module.css
│   │   └── Button.test.tsx
│   ├── Icon/
│   │   ├── Icon.tsx
│   │   ├── Icon.module.css
│   │   └── icons/
│   │       ├── SearchIcon.tsx
│   │       ├── PinIcon.tsx
│   │       ├── StarIcon.tsx
│   │       └── CloseIcon.tsx
│   ├── LoadingSpinner/
│   │   ├── LoadingSpinner.tsx
│   │   └── LoadingSpinner.module.css
│   ├── ErrorBoundary/
│   │   └── ErrorBoundary.tsx
│   ├── Portal/
│   │   └── Portal.tsx
│   ├── Card/
│   │   ├── Card.tsx
│   │   └── Card.module.css
│   ├── Input/
│   │   ├── Input.tsx
│   │   └── Input.module.css
│   └── Tooltip/
│       ├── Tooltip.tsx
│       └── Tooltip.module.css
├── Search/                  # Business logic components
│   ├── SearchBar.tsx        # Uses: Input, Icon
│   └── SearchResults.tsx    # Uses: Card, Icon
├── Map/
│   └── Map.tsx
├── Modal/
│   └── LocationModal.tsx    # Uses: Portal, Button, Icon, Card
└── Chart/
    └── TrafficChart.tsx
```

---

## Design System Foundation

### Colors
```typescript
export const colors = {
  primary: '#4285F4',
  primaryHover: '#3367D6',
  white: '#FFFFFF',
  gray100: '#f3f4f6',
  gray200: '#e5e7eb',
  gray300: '#d1d5db',
  gray600: '#6b7280',
  gray900: '#111827',
  error: '#ef4444',
  success: '#10b981',
};
```

### Spacing
```typescript
export const spacing = {
  xs: '4px',
  sm: '8px',
  md: '12px',
  lg: '16px',
  xl: '24px',
  xxl: '32px',
};
```

### Typography
```typescript
export const typography = {
  fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif',
  fontSize: {
    xs: '12px',
    sm: '14px',
    md: '16px',
    lg: '18px',
    xl: '20px',
  },
  fontWeight: {
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },
};
```

---

## Usage Examples

### Using Core Components in SearchBar
```typescript
import { Input } from '@components/core/Input/Input';
import { Icon } from '@components/core/Icon/Icon';
import { SearchIcon } from '@components/core/Icon/icons/SearchIcon';

const SearchBar: React.FC = () => {
  const { setQuery } = useSearch();

  return (
    <div className="search-bar">
      <Icon icon={SearchIcon} size="md" color="gray600" />
      <Input
        type="search"
        placeholder="Search..."
        onChange={(e) => setQuery(e.target.value)}
        aria-label="Search locations"
      />
    </div>
  );
};
```

### Using Core Components in LocationModal
```typescript
import { Button } from '@components/core/Button/Button';
import { Icon } from '@components/core/Icon/Icon';
import { Portal } from '@components/core/Portal/Portal';
import { Card } from '@components/core/Card/Card';

const LocationModal: React.FC = () => {
  const { selectedLocation, setSelectedLocation } = useLocations();

  const handleClose = useCallback(() => {
    setSelectedLocation(null);
  }, [setSelectedLocation]);

  if (!selectedLocation) return null;

  return (
    <Portal>
      <div className="modal-backdrop">
        <Card className="modal-card">
          <Button
            variant="icon"
            onClick={handleClose}
            aria-label="Close modal"
          >
            <Icon icon={CloseIcon} />
          </Button>
          
          <h2>{selectedLocation.name}</h2>
          
          {selectedLocation.details?.website && (
            <Button
              variant="primary"
              href={selectedLocation.details.website}
              target="_blank"
            >
              Visit Website
            </Button>
          )}
        </Card>
      </div>
    </Portal>
  );
};
```

---

## Next Steps

1. Review each core component design document
2. Implement core components first (Icon, Button, LoadingSpinner)
3. Use core components in application components
4. Maintain consistent design system
5. Add more core components as needed

Each core component design includes:
- Complete TypeScript interface
- Multiple variants/sizes
- Accessibility features
- Proper useCallback usage
- Testing examples
- Usage examples