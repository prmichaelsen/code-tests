import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.tsx';
import { UserProvider } from './contexts/UserContext';
import { StarredLocationsProvider } from './contexts/StarredLocationsContext';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <UserProvider>
      <StarredLocationsProvider>
        <App />
      </StarredLocationsProvider>
    </UserProvider>
  </StrictMode>
);