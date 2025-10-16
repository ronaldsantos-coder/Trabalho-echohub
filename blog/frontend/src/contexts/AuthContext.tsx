import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useToast } from '@/hooks/use-toast';
import axios from 'axios';

interface AuthContextType {
  isAuthenticated: boolean;
  username: string | null;
  userId: string | null;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

const API_BASE = '/api';

const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json'
  }
});

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState<string | null>(null);
  const [userId, setUserId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const { toast } = useToast();

  // Verifica sessão existente ao montar o componente
  useEffect(() => {
    const savedUsername = localStorage.getItem('username');
    const savedUserId = localStorage.getItem('userId');
    const isLoggedIn = localStorage.getItem('isAuthenticated') === 'true';

    if (savedUsername && savedUserId && isLoggedIn) {
      setUsername(savedUsername);
      setUserId(savedUserId);
      setIsAuthenticated(true);
    }
    setLoading(false);
  }, []);

  const login = async (usernameInput: string, password: string): Promise<boolean> => {
    try {
      setLoading(true);

      const response = await apiClient.post('/login', {
        username: usernameInput,
        password,
      });

      if (response.status === 200 && response.data.success) {
        const { token, user } = response.data;
        
        setIsAuthenticated(true);
        setUsername(user.username);
        setUserId(user.id);
        localStorage.setItem('username', user.username);
        localStorage.setItem('userId', user.id);
        localStorage.setItem('isAuthenticated', 'true');
        localStorage.setItem('authToken', token);

        toast({
          title: 'Login successful!',
          description: `Welcome back, ${user.username}`,
        });

        return true;
      } else {
        toast({
          variant: 'destructive',
          title: 'Login failed',
          description: response.data.error || 'Invalid credentials',
        });
        return false;
      }
    } catch (error: any) {
      console.error('Login error:', error);
      toast({
        variant: 'destructive',
        title: 'Login failed',
        description: error.response?.data?.error || 'Could not connect to server. Please try again.',
      });
      return false;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    setIsAuthenticated(false);
    setUsername(null);
    setUserId(null);
    localStorage.removeItem('username');
    localStorage.removeItem('userId');
    localStorage.removeItem('isAuthenticated');
    localStorage.removeItem('authToken');

    toast({
      title: 'Logged out',
      description: 'You have been logged out successfully',
    });
  };

  const value: AuthContextType = {
    isAuthenticated,
    username,
    userId,
    login,
    logout,
    loading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};