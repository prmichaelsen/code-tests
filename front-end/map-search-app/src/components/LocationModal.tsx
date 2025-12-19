import React, { useCallback, useEffect } from 'react';
import type { Location } from '../data/sampleData';
import pinIcon from '../assets/icon-pin.svg';
import './LocationModal.css';

interface LocationModalProps {
  location: Location | null;
  onClose: () => void;
}

const LocationModal: React.FC<LocationModalProps> = ({ location, onClose }) => {
  const handleClose = useCallback(() => {
    onClose();
  }, [onClose]);

  const handleBackdropClick = useCallback(
    (e: React.MouseEvent) => {
      if (e.target === e.currentTarget) {
        handleClose();
      }
    },
    [handleClose]
  );

  // Handle Escape key
  useEffect(() => {
    if (!location) return;

    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        handleClose();
      }
    };

    document.addEventListener('keydown', handleEscape);
    document.body.style.overflow = 'hidden';

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = '';
    };
  }, [location, handleClose]);

  if (!location) return null;

  return (
    <div className="modal-backdrop" onClick={handleBackdropClick}>
      <div className="modal-card">
        <div className="modal-header">
          <div className="modal-title">
            <img src={pinIcon} alt="" className="location-icon" />
            <div className="title-content">
              <h2>{location.name}</h2>
              <p className="location-coordinates">
                {location.location.lat.toFixed(6)}, {location.location.lon.toFixed(6)}
              </p>
            </div>
          </div>
          {location.details?.website && (
            <a href={location.details.website} target="_blank" rel="noopener noreferrer" className="visit-website-link">
              <button className="visit-website-button">Visit Website</button>
            </a>
          )}
        </div>

        <div className="modal-body">
          {location.details?.description && (
            <p className="description">{location.details.description}</p>
          )}

          {location.images && location.images.length > 0 && (
            <div className="image-gallery">
              {location.images.map((img, index) => (
                <img
                  key={index}
                  src={img}
                  alt={`${location.name} ${index + 1}`}
                  className="gallery-image"
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default LocationModal;