import React, { useState, useCallback } from 'react';
import Map from './components/Map';
import SearchBar from './components/SearchBar';
import SearchResults from './components/SearchResults';
import LocationModal from './components/LocationModal';
import type { Location } from './data/sampleData';
import { sampleData } from './data/sampleData';
import { searchLocations } from './utils/searchUtils';
import './App.css';

const App: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<Location[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [selectedLocation, setSelectedLocation] = useState<Location | null>(null);
  const [modalLocation, setModalLocation] = useState<Location | null>(null);

  const handleSearch = useCallback((query: string) => {
    setSearchQuery(query);
    
    if (!query.trim()) {
      setSearchResults([]);
      setHasSearched(false);
      setIsSearching(false);
      return;
    }

    setIsSearching(true);
    setHasSearched(true);

    // Simulate search delay for better UX
    setTimeout(() => {
      const results = searchLocations(sampleData, query);
      setSearchResults(results);
      setIsSearching(false);
    }, 200);
  }, []);

  const handleSelectLocation = useCallback((location: Location) => {
    setSelectedLocation(location);
    setSearchQuery(location.name); // Set search bar to location name
  }, []);

  const handleMarkerClick = useCallback((location: Location) => {
    setModalLocation(location);
  }, []);

  const handleCloseModal = useCallback(() => {
    setModalLocation(null);
  }, []);

  return (
    <div className="app">
      <div className="search-container">
        <SearchBar value={searchQuery} onSearch={handleSearch} />
        <SearchResults
          results={searchResults}
          isSearching={isSearching}
          hasSearched={hasSearched}
          onSelectLocation={handleSelectLocation}
          onOpenModal={handleMarkerClick}
        />
      </div>
      <Map 
        selectedLocation={selectedLocation} 
        searchResults={searchResults}
        onMarkerClick={handleMarkerClick} 
      />
      <LocationModal location={modalLocation} onClose={handleCloseModal} />
    </div>
  );
};

export default App;