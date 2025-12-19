import React, { useState, useCallback } from 'react';
import searchIcon from '../assets/icon-search.svg';
import './SearchBar.css';

interface SearchBarProps {
  value?: string;
  onSearch: (query: string) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ value = '', onSearch }) => {
  const [query, setQuery] = useState(value);

  // Update local state when value prop changes
  React.useEffect(() => {
    setQuery(value);
  }, [value]);

  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const value = e.target.value;
      setQuery(value);
      onSearch(value);
    },
    [onSearch]
  );

  const handleClear = useCallback(() => {
    setQuery('');
    onSearch('');
  }, [onSearch]);

  return (
    <div className="search-bar">
      <img src={searchIcon} alt="Search" className="search-icon" />
      <input
        type="text"
        value={query}
        onChange={handleChange}
        placeholder="Search..."
        className="search-input"
        aria-label="Search locations"
      />
      {query && (
        <button onClick={handleClear} className="clear-button" aria-label="Clear search">
          ×
        </button>
      )}
    </div>
  );
};

export default SearchBar;