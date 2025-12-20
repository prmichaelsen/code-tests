import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import type { ReactNode } from 'react';
import { useUser } from './UserContext';
import * as starService from '../services/starService';

interface StarredLocationsContextType {
  starredLocationIds: number[];
  isStarred: (id: number) => boolean;
  toggleStar: (id: number) => Promise<void>;
  starredCount: number;
  isLoading: boolean;
}

const StarredLocationsContext = createContext<StarredLocationsContextType | undefined>(undefined);

export const StarredLocationsProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const { user } = useUser();
  const [starredLocationIds, setStarredLocationIds] = useState<number[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Load starred locations from KV
  useEffect(() => {
    if (!user) return;

    const loadStarred = async () => {
      try {
        const ids = await starService.fetchStarredLocationIds(user.id);
        setStarredLocationIds(ids);
      } catch (error) {
        console.error('Failed to load starred locations:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadStarred();
  }, [user]);

  const isStarred = useCallback(
    (id: number) => {
      return starredLocationIds.includes(id);
    },
    [starredLocationIds]
  );

  const toggleStar = useCallback(
    async (locationId: number) => {
      if (!user) return;

      const wasStarred = starredLocationIds.includes(locationId);

      // Optimistic update
      setStarredLocationIds((prev) =>
        wasStarred ? prev.filter((id) => id !== locationId) : [...prev, locationId]
      );

      try {
        const response = await starService.toggleStar(user.id, locationId);
        // Update with server response
        setStarredLocationIds(response.starredLocationIds);
      } catch (error) {
        // Rollback on error
        setStarredLocationIds((prev) =>
          wasStarred ? [...prev, locationId] : prev.filter((id) => id !== locationId)
        );
        console.error('Failed to toggle star:', error);
        throw error;
      }
    },
    [user, starredLocationIds]
  );

  const value = {
    starredLocationIds,
    isStarred,
    toggleStar,
    starredCount: starredLocationIds.length,
    isLoading,
  };

  return (
    <StarredLocationsContext.Provider value={value}>
      {children}
    </StarredLocationsContext.Provider>
  );
};

export const useStarredLocations = () => {
  const context = useContext(StarredLocationsContext);
  if (!context) throw new Error('useStarredLocations must be used within StarredLocationsProvider');
  return context;
};