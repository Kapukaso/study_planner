import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';
import type { User, AuthState } from '../types';

interface AuthContextType extends AuthState {
  login: (token: string, user: User) => void;
  logout: () => void;
  updateUser: (user: User) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, setState] = useState<AuthState>({
    user: null,
    token: localStorage.getItem('token'),
    isAuthenticated: false,
    loading: true,
  });

  const login = (token: string, user: User) => {
    localStorage.setItem('token', token);
    setState({
      user,
      token,
      isAuthenticated: true,
      loading: false,
    });
  };

  const logout = () => {
    localStorage.removeItem('token');
    setState({
      user: null,
      token: null,
      isAuthenticated: false,
      loading: false,
    });
  };

  const updateUser = (user: User) => {
    setState((prev) => ({ ...prev, user }));
  };

  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        setState((prev) => ({ ...prev, loading: false }));
        return;
      }

      try {
        const response = await api.get('/api/auth/users/me');
        setState({
          user: response.data,
          token,
          isAuthenticated: true,
          loading: false,
        });
      } catch (error) {
        console.error('Auth initialization failed:', error);
        localStorage.removeItem('token');
        setState({
          user: null,
          token: null,
          isAuthenticated: false,
          loading: false,
        });
      }
    };

    initAuth();
  }, []);

  return (
    <AuthContext.Provider value={{ ...state, login, logout, updateUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
