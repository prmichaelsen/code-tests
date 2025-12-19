import React, { useCallback } from 'react';
import type { Location } from '../data/sampleData';
import pinIcon from '../assets/icon-pin.svg';
import './SearchResults.css';

interface SearchResultsProps {
  results: Location[];
  isSearching: boolean;
  hasSearched: boolean;
  onSelectLocation: (location: Location) => void;
  onOpenModal: (location: Location) => void;
}

const SearchResults: React.FC<SearchResultsProps> = ({
  results,
  isSearching,
  hasSearched,
  onSelectLocation,
  onOpenModal
}) => {
  const handleClick = useCallback(
    (location: Location) => {
      onSelectLocation(location);
      onOpenModal(location);
    },
    [onSelectLocation, onOpenModal]
  );

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent, location: Location) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        onSelectLocation(location);
        onOpenModal(location);
      }
    },
    [onSelectLocation, onOpenModal]
  );

  // Don't show anything if no search has been performed
  if (!hasSearched) {
    return null;
  }

  // Show loading state
  if (isSearching) {
    return (
      <div className="search-results">
        <div className="results-loading">Searching...</div>
      </div>
    );
  }

  // Show no results message
  if (results.length === 0) {
    return (
      <div className="search-results">
        <div className="no-results">No locations found</div>
      </div>
    );
  }

  // Show results
  return (
    <div className="search-results">
      <div className="results-header">
        Found {results.length} Result{results.length !== 1 ? 's' : ''}:
      </div>
      <div className="results-list">
        {results.map((location) => (
          <div
            key={location.id}
            className="result-item"
            onClick={() => handleClick(location)}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => handleKeyDown(e, location)}
          >
            <img src={pinIcon} alt="" className="result-icon" />
            <div className="result-info">
              <div className="result-name">{location.name}</div>
              <div className="result-coordinates">
                {location.location.lat.toFixed(6)}, {location.location.lon.toFixed(6)}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SearchResults;