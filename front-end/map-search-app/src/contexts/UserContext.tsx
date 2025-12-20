import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import type { ReactNode } from 'react';

interface User {
  id: string;
  isAnonymous: boolean;
}

interface UserContextType {
  user: User | null;
  resetUser: () => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

function getUserId(): string {
  const STORAGE_KEY = 'map-search-user-id';
  let userId = localStorage.getItem(STORAGE_KEY);
  
  if (!userId) {
    // Generate UUID v4 (fallback for browsers without crypto.randomUUID)
    userId = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
      const r = (Math.random() * 16) | 0;
      const v = c === 'x' ? r : (r & 0x3) | 0x8;
      return v.toString(16);
    });
    localStorage.setItem(STORAGE_KEY, userId);
  }
  
  return userId;
}

export const UserProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const userId = getUserId();
    setUser({ id: userId, isAnonymous: true });
  }, []);

  const resetUser = useCallback(() => {
    localStorage.removeItem('map-search-user-id');
    const newUserId = getUserId();
    setUser({ id: newUserId, isAnonymous: true });
  }, []);

  const value = { user, resetUser };

  return <UserContext.Provider value={value}>{children}</UserContext.Provider>;
};

export const useUser = () => {
  const context = useContext(UserContext);
  if (!context) throw new Error('useUser must be used within UserProvider');
  return context;
};