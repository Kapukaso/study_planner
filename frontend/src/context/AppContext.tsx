import React, { createContext, useContext, useState, useEffect } from 'react';
import type { Subject, Topic } from '../types';
import api from '../services/api';

interface AppContextType {
  subjects: Subject[];
  currentSubject: Subject | null;
  currentTopic: Topic | null;
  loading: boolean;
  setCurrentSubject: (subject: Subject | null) => void;
  setCurrentTopic: (topic: Topic | null) => void;
  refreshSubjects: () => Promise<void>;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [currentSubject, setCurrentSubject] = useState<Subject | null>(null);
  const [currentTopic, setCurrentTopic] = useState<Topic | null>(null);
  const [loading, setLoading] = useState(false);

  const refreshSubjects = async () => {
    setLoading(true);
    try {
      const response = await api.get('/api/subjects');
      setSubjects(response.data.subjects || []);
    } catch (error) {
      console.error('Failed to fetch subjects:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // For demo purposes, we'll always try to fetch subjects
    refreshSubjects();
  }, []);

  return (
    <AppContext.Provider
      value={{
        subjects,
        currentSubject,
        currentTopic,
        loading,
        setCurrentSubject,
        setCurrentTopic,
        refreshSubjects,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = () => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};
