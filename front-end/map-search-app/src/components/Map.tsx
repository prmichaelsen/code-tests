import React from 'react';
import { GoogleMap, Marker, useLoadScript } from '@react-google-maps/api';
import { sampleData } from '../data/sampleData';

const mapContainerStyle = {
  width: '100%',
  height: '100vh',
};

const center = {
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

const Map: React.FC = () => {
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY,
  });

  if (loadError) {
    return <div>Error loading maps</div>;
  }

  if (!isLoaded) {
    return <div>Loading maps...</div>;
  }

  return (
    <GoogleMap
      mapContainerStyle={mapContainerStyle}
      center={center}
      zoom={12}
      options={options}
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