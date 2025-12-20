import React, { useCallback } from 'react';
import { useStarredLocations } from '../contexts/StarredLocationsContext';
import './StarButton.css';

interface StarButtonProps {
  locationId: number;
}

const StarButton: React.FC<StarButtonProps> = ({ locationId }) => {
  const { isStarred, toggleStar } = useStarredLocations();
  const starred = isStarred(locationId);

  const handleClick = useCallback(
    async (e: React.MouseEvent) => {
      e.stopPropagation();

      try {
        await toggleStar(locationId);
      } catch (error) {
        console.error('Failed to toggle star:', error);
        alert('Failed to update favorite status');
      }
    },
    [locationId, toggleStar]
  );

  return (
    <button
      onClick={handleClick}
      className={`star-button ${starred ? 'starred' : ''}`}
      aria-label={starred ? 'Remove from favorites' : 'Add to favorites'}
      title={starred ? 'Remove from favorites' : 'Add to favorites'}
    >
      <span className="star-icon">{starred ? '★' : '☆'}</span>
      <span className="star-text">{starred ? 'Starred' : 'Star'}</span>
    </button>
  );
};

export default StarButton;