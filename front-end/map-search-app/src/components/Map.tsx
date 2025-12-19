import React, { useState, useCallback, useRef } from 'react';
import { GoogleMap, Marker, useLoadScript } from '@react-google-maps/api';
import type { Location } from '../data/sampleData';
import { sampleData } from '../data/sampleData';

const mapContainerStyle = {
  width: '100%',
  height: '100vh',
};

const defaultCenter = {
  lat: 42.354022,
  lng: -71.046245,
};

const options = {
  disableDefaultUI: false,
  zoomControl: true,
  mapTypeControl: false,
  streetViewControl: false,
  fullscreenControl: false,
};

interface MapProps {
  selectedLocation: Location | null;
}

const Map: React.FC<MapProps> = ({ selectedLocation }) => {
  const [map, setMap] = useState<google.maps.Map | null>(null);
  
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY,
  });

  // Pan to selected location
  React.useEffect(() => {
    if (map && selectedLocation) {
      map.panTo({
        lat: selectedLocation.location.lat,
        lng: selectedLocation.location.lon,
      });
      map.setZoom(15);
    }
  }, [map, selectedLocation]);

  const onLoad = useCallback((mapInstance: google.maps.Map) => {
    setMap(mapInstance);
  }, []);

  if (loadError) {
    return <div>Error loading maps</div>;
  }

  if (!isLoaded) {
    return <div>Loading maps...</div>;
  }

  return (
    <GoogleMap
      mapContainerStyle={mapContainerStyle}
      center={defaultCenter}
      zoom={12}
      options={options}
      onLoad={onLoad}
    >
      {sampleData.map((location) => (
        <Marker
          key={location.id}
          position={{
            lat: location.location.lat,
            lng: location.location.lon,
          }}
          title={location.name}
        />
      ))}
    </GoogleMap>
  );
};

export default Map;