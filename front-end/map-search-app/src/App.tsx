import React, { useState, useCallback } from 'react';
import Map from './components/Map';
import SearchBar from './components/SearchBar';
import SearchResults from './components/SearchResults';
import type { Location } from './data/sampleData';
import { sampleData } from './data/sampleData';
import { searchLocations } from './utils/searchUtils';
import './App.css';

const App: React.FC = () => {
  const [searchResults, setSearchResults] = useState<Location[]>([]);
  const [selectedLocation, setSelectedLocation] = useState<Location | null>(null);

  const handleSearch = useCallback((query: string) => {
    if (!query.trim()) {
      setSearchResults([]);
      return;
    }

    const results = searchLocations(sampleData, query);
    setSearchResults(results);
  }, []);

  const handleSelectLocation = useCallback((location: Location) => {
    setSelectedLocation(location);
    setSearchResults([]); // Close results after selection
  }, []);

  return (
    <div className="app">
      <div className="search-container">
        <SearchBar onSearch={handleSearch} />
        <SearchResults results={searchResults} onSelectLocation={handleSelectLocation} />
      </div>
      <Map selectedLocation={selectedLocation} />
    </div>
  );
};

export default App;