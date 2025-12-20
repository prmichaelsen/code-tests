// Mock star service using localStorage

const STORAGE_KEY = 'map-search-starred';

interface UserStarData {
  userId: string;
  starredLocationIds: number[];
  updatedAt: number;
}

function getStarredData(userId: string): UserStarData {
  const data = localStorage.getItem(`${STORAGE_KEY}-${userId}`);
  if (!data) {
    return { userId, starredLocationIds: [], updatedAt: Date.now() };
  }
  return JSON.parse(data);
}

function saveStarredData(data: UserStarData): void {
  localStorage.setItem(`${STORAGE_KEY}-${data.userId}`, JSON.stringify(data));
}

/**
 * Fetch user's starred location IDs from localStorage
 */
export async function fetchStarredLocationIds(userId: string): Promise<number[]> {
  // Simulate network delay
  await new Promise(resolve => setTimeout(resolve, 100));
  
  const data = getStarredData(userId);
  return data.starredLocationIds;
}

/**
 * Toggle star status for a location
 */
export async function toggleStar(
  userId: string,
  locationId: number
): Promise<UserStarData> {
  // Simulate network delay
  await new Promise(resolve => setTimeout(resolve, 100));
  
  const data = getStarredData(userId);
  
  const index = data.starredLocationIds.indexOf(locationId);
  if (index > -1) {
    data.starredLocationIds.splice(index, 1);
  } else {
    data.starredLocationIds.push(locationId);
  }
  
  data.updatedAt = Date.now();
  saveStarredData(data);
  
  return data;
}