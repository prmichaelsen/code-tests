import React, { useCallback } from 'react';
import type { Location } from '../data/sampleData';
import pinIcon from '../assets/icon-pin.svg';
import './SearchResults.css';

interface SearchResultsProps {
  results: Location[];
  onSelectLocation: (location: Location) => void;
}

const SearchResults: React.FC<SearchResultsProps> = ({ results, onSelectLocation }) => {
  const handleClick = useCallback(
    (location: Location) => {
      onSelectLocation(location);
    },
    [onSelectLocation]
  );

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent, location: Location) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        onSelectLocation(location);
      }
    },
    [onSelectLocation]
  );

  if (results.length === 0) {
    return null;
  }

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