# LocationModal Component Design

## Overview
A centered modal that displays detailed information about a selected location, including name, coordinates, description, website link, images, and optional traffic chart.

## Visual Design (from test-example-modal.png)
- **Position**: Centered both horizontally and vertically
- **Size**: ~600px width, variable height
- **Backdrop**: Dark semi-transparent overlay (rgba(0, 0, 0, 0.5))
- **Card**: White background, rounded corners (8px), shadow
- **Close Button**: X icon in top-right corner

## Props Interface
```typescript
interface LocationModalProps {
  location: Location | null;
  isOpen: boolean;
  onClose: () => void;
  onStar?: (locationId: number) => void;
}
```

## State Management
- Uses `ModalContext` for modal state (or local state)
- Uses `LocationContext` for selected location
- Local state for image carousel/gallery

## Modal Structure
```
┌────────────────────────────────────────┐
│ 📍 Alberts Bike Shop           [X]     │ ← Header
│    42.354022, -71.046245               │
├────────────────────────────────────────┤
│                                        │
│ [Visit Website] button (blue)         │ ← Actions
│                                        │
│ We buy and sell used bikes and         │ ← Description
│ equipment. Contact us today to get     │
│ moving!                                │
│                                        │
│ ┌────┐ ┌────┐ ┌────┐                  │ ← Image Gallery
│ │img1│ │img2│ │img3│                  │
│ └────┘ └────┘ └────┘                  │
│                                        │
│ [Chart] (if avgStoreTraffic exists)   │ ← Optional Chart
│                                        │
└────────────────────────────────────────┘
```

## Styling
```css
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  animation: fadeIn 0.2s ease-out;
}

.modal-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  animation: slideUp 0.3s ease-out;
}

.modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 24px;
  border-bottom: 1px solid #e5e7eb;
}

.modal-title-section {
  flex: 1;
}

.modal-title {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 0 0 8px 0;
}

.location-icon {
  width: 24px;
  height: 24px;
  color: #4285F4;
}

.location-name {
  font-size: 20px;
  font-weight: 600;
  color: #111827;
}

.location-coordinates {
  font-size: 14px;
  color: #6b7280;
  margin-left: 36px; /* Align with name */
}

.close-button {
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  color: #6b7280;
  border-radius: 4px;
  transition: all 0.2s;
}

.close-button:hover {
  background: #f3f4f6;
  color: #111827;
}

.modal-body {
  padding: 24px;
}

.visit-website-button {
  background: #4285F4;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  margin-bottom: 20px;
  transition: background 0.2s;
}

.visit-website-button:hover {
  background: #3367D6;
}

.description {
  font-size: 16px;
  line-height: 1.6;
  color: #374151;
  margin-bottom: 24px;
}

.image-gallery {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 24px;
}

.gallery-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 6px;
  cursor: pointer;
  transition: transform 0.2s;
}

.gallery-image:hover {
  transform: scale(1.05);
}

.chart-container {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}

.chart-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #111827;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
```

## Component Structure
```typescript
const LocationModal: React.FC = () => {
  const { selectedLocation, setSelectedLocation } = useLocations();
  const isOpen = selectedLocation !== null;

  // ✅ Properly wrapped with useCallback
  const handleClose = useCallback(() => {
    setSelectedLocation(null);
  }, [setSelectedLocation]); // From LocationContext (stable)

  // ✅ Properly wrapped with useCallback
  const handleBackdropClick = useCallback((e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      handleClose();
    }
  }, [handleClose]); // handleClose is stable (memoized above)

  if (!isOpen || !selectedLocation) return null;

  // ✅ Simple rendering - no portal needed
  return (
    <div className="modal-backdrop" onClick={handleBackdropClick}>
      <div className="modal-card">
        <div className="modal-header">
          <div className="modal-title-section">
            <div className="modal-title">
              <LocationIcon />
              <h2>{selectedLocation.name}</h2>
            </div>
            <p className="location-coordinates">
              {selectedLocation.location.lat}, {selectedLocation.location.lon}
            </p>
          </div>
          <button className="close-button" onClick={handleClose}>
            <CloseIcon />
          </button>
        </div>

        <div className="modal-body">
          {selectedLocation.details?.website && (
            <a
              href={selectedLocation.details.website}
              target="_blank"
              rel="noopener noreferrer"
            >
              <button className="visit-website-button">
                Visit Website
              </button>
            </a>
          )}

          {selectedLocation.details?.description && (
            <p className="description">
              {selectedLocation.details.description}
            </p>
          )}

          {selectedLocation.images && selectedLocation.images.length > 0 && (
            <div className="image-gallery">
              {selectedLocation.images.map((img, index) => (
                <img
                  key={index}
                  src={img}
                  alt={`${selectedLocation.name} ${index + 1}`}
                  className="gallery-image"
                />
              ))}
            </div>
          )}

          {selectedLocation.details?.avgStoreTraffic && (
            <div className="chart-container">
              <h3 className="chart-title">Average Store Traffic</h3>
              <TrafficChart data={selectedLocation.details.avgStoreTraffic} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
```

## Accessibility
- `role="dialog"`
- `aria-modal="true"`
- `aria-labelledby` for title
- Focus trap (keep focus within modal)
- Escape key to close
- Focus management (restore focus on close)
- Keyboard navigation

## Interactions
1. **Open**: Triggered when marker is clicked
2. **Close**: 
   - Click X button
   - Click backdrop
   - Press Escape key
3. **Visit Website**: Opens in new tab
4. **View Images**: Click to open full-size (optional lightbox)
5. **Star Location**: Toggle favorite status (optional)

## Simple Rendering (No Portal Needed)
```typescript
// ✅ Simple: Just render in place with high z-index
// No need for createPortal for this simple modal

if (!isOpen || !selectedLocation) return null;

return (
  <div className="modal-backdrop">
    <div className="modal-card">
      {/* Modal content */}
    </div>
  </div>
);
```

**Why no portal needed:**
- Modal has `z-index: 2000` (higher than everything else)
- Backdrop covers entire viewport with `position: fixed`
- No complex z-index stacking issues in this simple app
- Simpler code, easier to understand

## Focus Management
```typescript
useEffect(() => {
  if (isOpen) {
    // Store current focus
    previousFocusRef.current = document.activeElement;
    
    // Focus modal
    modalRef.current?.focus();
    
    // Prevent body scroll
    document.body.style.overflow = 'hidden';
  } else {
    // Restore focus
    previousFocusRef.current?.focus();
    
    // Restore scroll
    document.body.style.overflow = '';
  }
}, [isOpen]);
```

## Image Gallery Enhancement
```typescript
const [lightboxOpen, setLightboxOpen] = useState(false);
const [currentImageIndex, setCurrentImageIndex] = useState(0);

// ✅ Properly wrapped with useCallback
const handleImageClick = useCallback((index: number) => {
  setCurrentImageIndex(index);
  setLightboxOpen(true);
}, []); // Only uses setState (always stable)

// Optional: Add image lightbox/carousel
```

## Dependencies
- `SelectedLocationContext` for selected location
- `TrafficChart` component (optional)
- `icon-pin.svg` for location icon
- No portal needed - simple fixed positioning with high z-index

## File Location
`src/components/Modal/LocationModal.tsx`
`src/components/Modal/LocationModal.module.css`

## Responsive Design
```css
@media (max-width: 640px) {
  .modal-card {
    width: 100%;
    max-width: 100%;
    height: 100vh;
    max-height: 100vh;
    border-radius: 0;
  }

  .image-gallery {
    grid-template-columns: 1fr; /* Stack images on mobile */
  }
}
```

## Testing Considerations
- Test with locations that have all fields
- Test with minimal location data (no images, no description)
- Test with missing website
- Test with avgStoreTraffic data
- Test keyboard navigation
- Test focus management
- Test on mobile devices