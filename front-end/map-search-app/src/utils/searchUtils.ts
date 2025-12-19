import Fuse from 'fuse.js';
import type { Location } from '../data/sampleData';

/**
 * Search locations using fuzzy search
 * Searches in name and description with typo tolerance
 */
export function searchLocations(locations: Location[], query: string): Location[] {
  const trimmedQuery = query.trim();
  
  if (!trimmedQuery) {
    return [];
  }

  // Configure Fuse.js for fuzzy search
  const fuse = new Fuse(locations, {
    keys: [
      { name: 'name', weight: 2 }, // Name is more important
      { name: 'details.description', weight: 1 },
    ],
    threshold: 0.3, // 0 = exact match, 1 = match anything
    includeScore: true,
    minMatchCharLength: 2,
  });

  const results = fuse.search(trimmedQuery);
  
  // Return just the items (not the Fuse result objects)
  return results.map((result) => result.item);
}