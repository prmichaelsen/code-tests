# SearchBar Component Design

## Overview
A search input component with icon that allows users to search for locations by name. Provides real-time autocomplete functionality.

## Visual Design
- **Position**: Fixed top-left corner of the screen
- **Size**: ~400px width, ~50px height
- **Style**: White background, rounded corners (8px), subtle shadow
- **Icon**: Magnifying glass icon on the left side
- **Placeholder**: "Search..."

## Props Interface
```typescript
interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  onFocus?: () => void;
  onBlur?: () => void;
  placeholder?: string;
  className?: string;
}
```

## State Management
- Uses `SearchContext` for global search state
- Local state for input focus
- Debounced search (300ms) to avoid excessive filtering

## Behavior
1. **User Types**: Updates search query in context
2. **Debouncing**: Waits 300ms after last keystroke before filtering
3. **Focus**: Shows results dropdown when focused and has results
4. **Blur**: Hides results dropdown (with delay for click handling)
5. **Clear**: Clicking X icon clears search

## Styling
```css
.search-bar {
  position: fixed;
  top: 20px;
  left: 20px;
  z-index: 1000;
  width: 400px;
}

.search-input-container {
  display: flex;
  align-items: center;
  background: white;
  border-radius: 8px;
  padding: 12px 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.search-icon {
  width: 20px;
  height: 20px;
  margin-right: 12px;
  color: #666;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 16px;
  color: #333;
}

.search-input::placeholder {
  color: #999;
}
```

## Accessibility
- `role="search"`
- `aria-label="Search locations"`
- `aria-expanded` for dropdown state
- `aria-controls` linking to results dropdown
- Keyboard navigation support (Arrow keys, Enter, Escape)

## Dependencies
- `SearchContext` for state management
- `icon-search.svg` for search icon
- `SearchResults` component (sibling)

## File Location
`src/components/Search/SearchBar.tsx`
`src/components/Search/SearchBar.module.css`