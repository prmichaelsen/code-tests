# React Hooks Best Practices

## useCallback Usage Guidelines

### When to Use useCallback

**✅ ALWAYS use `useCallback` when:**

1. **Passing callbacks to child components**
```typescript
// ✅ Good: Prevents child re-renders
const handleClick = useCallback(() => {
  doSomething();
}, []);

<ChildComponent onClick={handleClick} />
```

2. **Callbacks used in useEffect dependencies**
```typescript
// ✅ Good: Stable reference prevents infinite loops
const fetchData = useCallback(async () => {
  const data = await api.get('/data');
  setData(data);
}, []);

useEffect(() => {
  fetchData();
}, [fetchData]); // Won't cause infinite loop
```

3. **Callbacks passed to context**
```typescript
// ✅ Good: Context consumers won't re-render unnecessarily
const toggleStar = useCallback(async (id: number) => {
  await locationService.toggleStarLocation(id);
}, []);

const value = {
  toggleStar, // Stable reference
};
```

4. **Event handlers in frequently re-rendering components**
```typescript
// ✅ Good: Prevents creating new function on every render
const SearchBar: React.FC = () => {
  const [query, setQuery] = useState('');

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value);
  }, []);

  return <input onChange={handleChange} />;
};
```

### When NOT to Use useCallback

**❌ DON'T use `useCallback` when:**

1. **Simple event handlers not passed as props**
```typescript
// ❌ Unnecessary: Not passed to children
const handleClick = useCallback(() => {
  console.log('clicked');
}, []);

// ✅ Better: Just use inline
<button onClick={() => console.log('clicked')}>Click</button>
```

2. **Callbacks that change on every render anyway**
```typescript
// ❌ Pointless: Dependencies change every render
const handleClick = useCallback(() => {
  console.log(someValue);
}, [someValue]); // someValue changes every render

// ✅ Better: Just use regular function
const handleClick = () => {
  console.log(someValue);
};
```

3. **Inside loops or conditional rendering**
```typescript
// ❌ Bad: useCallback in loop
items.map(item => {
  const handleClick = useCallback(() => {
    doSomething(item.id);
  }, [item.id]); // Violates Rules of Hooks
  
  return <button onClick={handleClick} />;
});

// ✅ Better: Extract to separate component
const Item: React.FC<{ item: Item }> = ({ item }) => {
  const handleClick = useCallback(() => {
    doSomething(item.id);
  }, [item.id]);
  
  return <button onClick={handleClick} />;
};
```

---

## Correct useCallback Patterns

### Pattern 1: Context Callbacks

```typescript
export const LocationProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, setState] = useState<LocationState>({
    locations: [],
    selectedLocation: null,
    starredLocations: [],
  });

  // ✅ All callbacks wrapped with useCallback
  const setSelectedLocation = useCallback((location: Location | null) => {
    setState(prev => ({ ...prev, selectedLocation: location }));
  }, []); // Empty deps: only uses setState (always stable)

  const toggleStar = useCallback(async (locationId: number) => {
    try {
      const updated = await toggleStarLocation(locationId);
      setState(prev => ({
        ...prev,
        locations: prev.locations.map(loc =>
          loc.id === locationId ? updated : loc
        ),
        starredLocations: updated.starred
          ? [...prev.starredLocations, updated]
          : prev.starredLocations.filter(loc => loc.id !== locationId),
      }));
    } catch (error) {
      console.error('Failed to toggle star:', error);
    }
  }, []); // Empty deps: only uses setState

  const addLocation = useCallback(async (location: Omit<Location, 'id'>) => {
    const newLocation = await createLocation(location);
    setState(prev => ({
      ...prev,
      locations: [...prev.locations, newLocation],
    }));
  }, []); // Empty deps: only uses setState

  const updateLocation = useCallback(async (id: number, updates: Partial<Location>) => {
    const updated = await locationService.updateLocation(id, updates);
    setState(prev => ({
      ...prev,
      locations: prev.locations.map(loc => (loc.id === id ? updated : loc)),
    }));
  }, []); // Empty deps: only uses setState

  const deleteLocation = useCallback(async (id: number) => {
    await locationService.deleteLocation(id);
    setState(prev => ({
      ...prev,
      locations: prev.locations.filter(loc => loc.id !== id),
      starredLocations: prev.starredLocations.filter(loc => loc.id !== id),
    }));
  }, []); // Empty deps: only uses setState

  const value: LocationContextType = {
    ...state,
    setSelectedLocation,
    toggleStar,
    addLocation,
    updateLocation,
    deleteLocation,
  };

  return <LocationContext.Provider value={value}>{children}</LocationContext.Provider>;
};
```

### Pattern 2: Component Event Handlers

```typescript
const SearchBar: React.FC = () => {
  const { setQuery } = useSearch();
  const [localValue, setLocalValue] = useState('');

  // ✅ useCallback for handler passed to child/DOM
  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setLocalValue(value);
    setQuery(value);
  }, [setQuery]); // setQuery from context (stable)

  const handleClear = useCallback(() => {
    setLocalValue('');
    setQuery('');
  }, [setQuery]); // setQuery from context (stable)

  return (
    <div className="search-bar">
      <input
        value={localValue}
        onChange={handleChange}
        placeholder="Search..."
      />
      {localValue && (
        <button onClick={handleClear}>×</button>
      )}
    </div>
  );
};
```

### Pattern 3: useEffect Dependencies

```typescript
const SearchResults: React.FC = () => {
  const { query, results } = useSearch();
  const { setSelectedLocation } = useLocations();
  const { panTo } = useMap();

  // ✅ useCallback for function used in useEffect
  const handleSelectLocation = useCallback((location: Location) => {
    setSelectedLocation(location);
    panTo({ lat: location.location.lat, lng: location.location.lon });
  }, [setSelectedLocation, panTo]); // Both from context (stable)

  // Now handleSelectLocation is stable and safe to use in useEffect
  useEffect(() => {
    // Some effect that uses handleSelectLocation
  }, [handleSelectLocation]);

  return (
    <div className="results">
      {results.map(location => (
        <div
          key={location.id}
          onClick={() => handleSelectLocation(location)}
        >
          {location.name}
        </div>
      ))}
    </div>
  );
};
```

### Pattern 4: Memoized Child Components

```typescript
const LocationList: React.FC = () => {
  const { locations } = useLocations();

  // ✅ useCallback for prop passed to memoized component
  const handleLocationClick = useCallback((id: number) => {
    console.log('Clicked location:', id);
  }, []);

  return (
    <div>
      {locations.map(location => (
        <MemoizedLocationCard
          key={location.id}
          location={location}
          onClick={handleLocationClick} // Stable reference
        />
      ))}
    </div>
  );
};

// Memoized component won't re-render if props don't change
const MemoizedLocationCard = React.memo(LocationCard);
```

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Missing Dependencies

```typescript
// ❌ Bad: Missing dependency
const handleClick = useCallback(() => {
  doSomething(someValue);
}, []); // someValue not in deps!

// ✅ Good: Include all dependencies
const handleClick = useCallback(() => {
  doSomething(someValue);
}, [someValue]);
```

### ❌ Mistake 2: Unnecessary useCallback

```typescript
// ❌ Unnecessary: Not passed to children or used in effects
const MyComponent = () => {
  const handleClick = useCallback(() => {
    console.log('clicked');
  }, []);

  return <button onClick={handleClick}>Click</button>;
};

// ✅ Better: Just use inline
const MyComponent = () => {
  return <button onClick={() => console.log('clicked')}>Click</button>;
};
```

### ❌ Mistake 3: useCallback in Loops

```typescript
// ❌ Bad: Violates Rules of Hooks
items.map(item => {
  const handleClick = useCallback(() => {
    doSomething(item.id);
  }, [item.id]);
  
  return <button onClick={handleClick} />;
});

// ✅ Good: Extract to component
const Item: React.FC<{ item: Item }> = ({ item }) => {
  const handleClick = useCallback(() => {
    doSomething(item.id);
  }, [item.id]);
  
  return <button onClick={handleClick} />;
};

// Then use:
items.map(item => <Item key={item.id} item={item} />);
```

---

## ESLint Rule

Enable the exhaustive-deps rule:

```javascript
// .eslintrc.cjs
module.exports = {
  rules: {
    'react-hooks/exhaustive-deps': 'warn',
  },
};
```

This will warn you if you forget dependencies in `useCallback`, `useMemo`, or `useEffect`.

---

## Performance Benefits

### Without useCallback:
```typescript
// New function created on EVERY render
const Parent = () => {
  const handleClick = () => console.log('clicked');
  return <ExpensiveChild onClick={handleClick} />; // Re-renders every time!
};
```

### With useCallback:
```typescript
// Same function reference across renders
const Parent = () => {
  const handleClick = useCallback(() => {
    console.log('clicked');
  }, []); // Stable reference
  
  return <ExpensiveChild onClick={handleClick} />; // Only re-renders when needed
};

const ExpensiveChild = React.memo(({ onClick }) => {
  // Expensive rendering logic
  return <button onClick={onClick}>Click</button>;
});
```

---

## Summary: useCallback Checklist

### ✅ Use useCallback when:
- [ ] Passing callback to child component
- [ ] Callback used in useEffect/useMemo dependencies
- [ ] Callback passed to context
- [ ] Callback passed to memoized component
- [ ] Component re-renders frequently

### ❌ Don't use useCallback when:
- [ ] Simple inline handlers not passed as props
- [ ] Dependencies change every render anyway
- [ ] Inside loops or conditions
- [ ] Premature optimization

### 🎯 Rule of Thumb:
**If a function is passed as a prop or used as a dependency, wrap it in `useCallback`.**

---

## All Context Callbacks Should Use useCallback

### LocationContext ✅
```typescript
const setSelectedLocation = useCallback(..., []);
const toggleStar = useCallback(..., []);
const addLocation = useCallback(..., []);
const updateLocation = useCallback(..., []);
const deleteLocation = useCallback(..., []);
```

### SearchContext ✅
```typescript
const setQuery = useCallback(..., []);
const clearSearch = useCallback(..., []);
```

### MapContext ✅
```typescript
const setCenter = useCallback(..., []);
const setZoom = useCallback(..., []);
const setMapInstance = useCallback(..., []);
const panTo = useCallback(..., [state.mapInstance, setCenter]);
```

This ensures stable references and prevents unnecessary re-renders throughout the app!