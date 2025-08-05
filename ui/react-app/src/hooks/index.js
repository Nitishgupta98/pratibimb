import { useState, useEffect, useCallback } from 'react';
import { fetchPratibimbData } from '../services/api';

export const useData = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await fetchPratibimbData();
      setData(result);
    } catch (err) {
      setError(err.message);
      console.error('Error loading data:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const refreshData = async () => {
    await loadData();
  };

  return { data, loading, error, refreshData };
};

export const useSidebar = () => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth <= 768);
      if (window.innerWidth <= 768) {
        setIsCollapsed(true);
      }
    };

    checkMobile();
    window.addEventListener('resize', checkMobile);

    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const toggleSidebar = () => {
    setIsCollapsed(!isCollapsed);
  };

  const closeSidebar = () => {
    if (isMobile) {
      setIsCollapsed(true);
    }
  };

  return { isCollapsed, isMobile, toggleSidebar, closeSidebar };
};

export const useConversion = () => {
  const [conversionHistory, setConversionHistory] = useState([]);
  const [isConverting, setIsConverting] = useState(false);

  const addConversion = (conversion) => {
    const newConversion = {
      id: Date.now().toString(),
      timestamp: new Date().toISOString(),
      ...conversion
    };
    setConversionHistory(prev => [newConversion, ...prev]);
    return newConversion;
  };

  const removeConversion = (id) => {
    setConversionHistory(prev => prev.filter(conv => conv.id !== id));
  };

  const clearHistory = () => {
    setConversionHistory([]);
  };

  return {
    conversionHistory,
    isConverting,
    setIsConverting,
    addConversion,
    removeConversion,
    clearHistory
  };
};

export const useLocalStorage = (key, initialValue) => {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  });

  const setValue = (value) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(`Error setting localStorage key "${key}":`, error);
    }
  };

  const removeValue = () => {
    try {
      window.localStorage.removeItem(key);
      setStoredValue(initialValue);
    } catch (error) {
      console.error(`Error removing localStorage key "${key}":`, error);
    }
  };

  return [storedValue, setValue, removeValue];
};
