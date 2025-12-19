# Front-End Tasks

## Overview
This directory contains front-end interview tests focused on building interactive map-based search interfaces using React and Google Maps API.

## Test 1: Map Search Application

### Core Requirements

#### 1. Setup & Configuration
- [ ] Set up React development environment
- [ ] Configure Google Maps API integration
- [ ] Import and structure sample data from [`sample-data.js`](../map-search-test/sample-data.js)
- [ ] Set up project structure with components

#### 2. Autocomplete Search Field
- [ ] Create search input component
- [ ] Implement real-time autocomplete functionality
- [ ] Filter results based on `name` field from sample data
- [ ] Display "no results" message when search yields nothing
- [ ] Match design from [`test-example-search.png`](../map-search-test/test-example-search.png)

#### 3. Results List
- [ ] Create results list component
- [ ] Display filtered search results
- [ ] Make results clickable/selectable
- [ ] Handle result selection to trigger map interaction

#### 4. Map Integration
- [ ] Initialize Google Maps in React
- [ ] Display markers for locations
- [ ] Handle marker clicks to show details
- [ ] Center/zoom map when location is selected from search
- [ ] Use provided [`icon-pin.svg`](../map-search-test/icon-pin.svg) for markers

#### 5. Details Modal
- [ ] Create modal component
- [ ] Display location details when marker is clicked
- [ ] Center modal both horizontally and vertically
- [ ] Match design from [`test-example-modal.png`](../map-search-test/test-example-modal.png)
- [ ] Include close functionality

#### 6. Star/Favorite Feature
- [ ] Implement ability to "star" locations
- [ ] Save starred locations to a list
- [ ] Create shareable list functionality
- [ ] Persist starred locations (localStorage or similar)

#### 7. Mock API Server & CRUD Operations
- [ ] Set up mock API server (json-server, MSW, or similar)
- [ ] Implement GET endpoint for locations
- [ ] Implement POST endpoint to add new locations
- [ ] Implement PUT/PATCH endpoint to edit locations
- [ ] Implement DELETE endpoint to remove locations
- [ ] Support fields: title, description, images, link, etc.

### Extra Credit

#### Chart Integration
- [ ] Install Chart.js library
- [ ] Create chart component for `avgStoreTraffic` data
- [ ] Integrate chart into details modal
- [ ] Style chart to match overall design

#### Additional Enhancements
- [ ] Add loading states for async operations
- [ ] Implement error handling
- [ ] Add animations/transitions
- [ ] Optimize performance for large datasets
- [ ] Add unit tests for components
- [ ] Improve accessibility (ARIA labels, keyboard navigation)

### Documentation Requirements
- [ ] Document why React was chosen (or alternative framework)
- [ ] Explain library/framework choices
- [ ] Document any trade-offs or limitations
- [ ] Add inline code comments for complex logic
- [ ] Create README with setup instructions

### Design Matching
- [ ] Match initial page layout from [`test-example-start.png`](../map-search-test/test-example-start.png)
- [ ] Use provided SVG icons ([`icon-search.svg`](../map-search-test/icon-search.svg), [`icon-pin.svg`](../map-search-test/icon-pin.svg))
- [ ] Ensure responsive design
- [ ] Match color scheme and typography

## Files to Modify/Create

### Existing Files
- [`index.html`](../map-search-test/index.html) - Update to support React
- [`main.css`](../map-search-test/main.css) - Add styles for components
- [`main.js`](../map-search-test/main.js) - Replace with React application
- [`sample-data.js`](../map-search-test/sample-data.js) - Use as data source

### New Files to Create
- `package.json` - Dependencies and scripts
- `src/App.jsx` - Main React component
- `src/components/SearchBar.jsx` - Search input component
- `src/components/ResultsList.jsx` - Search results component
- `src/components/Map.jsx` - Google Maps wrapper
- `src/components/Modal.jsx` - Details modal component
- `src/components/Chart.jsx` - Chart.js integration (extra credit)
- `src/api/mockServer.js` - Mock API server setup
- `src/utils/` - Helper functions
- `README.md` - Setup and documentation

## Resources
- [React Documentation](https://react.dev/)
- [Google Maps JavaScript API](https://developers.google.com/maps/documentation/javascript/)
- [Chart.js Documentation](http://chartjs.org/)

## Time Estimate
- Core functionality: 3-4 hours
- Extra credit features: 1-2 hours
- Total: 4-6 hours

## Success Criteria
- All core requirements implemented and functional
- Design closely matches provided mockups
- Code is well-documented and maintainable
- CRUD operations work correctly with mock API
- Application is responsive and user-friendly