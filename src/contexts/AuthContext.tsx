import React, { createContext, ReactNode, useContext, useEffect, useState } from 'react';
import { authService } from '../services/api';
import { User } from '../types/index';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (usernameOrEmail: string, password: string) => Promise<boolean>;
  register: (username: string, email: string, password: string) => Promise<boolean>;
  logout: () => void;
  updateUser: (userData: Partial<User>) => void;
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

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initializeAuth = async () => {
      try {
        // First check if we have a token in localStorage
        const token = localStorage.getItem('auth_token');
        const userStr = localStorage.getItem('user');

        if (token && userStr) {
          try {
            // Try to parse stored user data
            const storedUser = JSON.parse(userStr);

            // Verify token is still valid by calling /auth/me
            const currentUser = await authService.getCurrentUser();
            if (currentUser) {
              setUser(currentUser);
            } else {
              // Token invalid, clear storage
              localStorage.removeItem('auth_token');
              localStorage.removeItem('user');
            }
          } catch (error) {
            // Invalid stored data, clear it
            localStorage.removeItem('auth_token');
            localStorage.removeItem('user');
          }
        }
        // If no token/user, user stays null (not logged in)
      } catch (error) {
        console.error('Failed to initialize auth:', error);
        // Clear potentially corrupted data
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user');
      } finally {
        setLoading(false);
      }
    };

    initializeAuth();
  }, []);

  const login = async (usernameOrEmail: string, password: string): Promise<boolean> => {
    try {
      console.log('🔐 AuthContext: Starting login process');
      console.log('📧 Username/Email:', usernameOrEmail);
      console.log('🔑 Password:', password ? '***provided***' : 'NOT PROVIDED');

      const response = await authService.login({ usernameOrEmail, password });

      console.log('📡 AuthService response:', response);

      if (response.success && response.data) {
        console.log('✅ Login successful, setting user:', response.data.user);
        setUser(response.data.user);
        return true;
      } else {
        console.log('❌ Login failed:', response.error || 'Unknown error');
        return false;
      }
    } catch (error) {
      console.error('❌ Login exception:', error);
      return false;
    }
  };

  const register = async (username: string, email: string, password: string): Promise<boolean> => {
    try {
      console.log('AuthContext: Starting registration process');
      console.log('Username:', username);
      console.log('Email:', email);
      console.log('Password:', password ? '***provided***' : 'NOT PROVIDED');

      const response = await authService.register({
        username,
        email,
        password,
        confirmPassword: password
      });

      console.log('AuthService registration response:', response);

      if (response.success && response.data) {
        console.log('Registration successful');
        // Don't automatically log in after registration
        // User should go back to login page to enter their credentials
        return true;
      } else {
        console.log('Registration failed:', response.error || 'Unknown error');
        return false;
      }
    } catch (error) {
      console.error('Registration exception:', error);
      return false;
    }
  };

  const logout = () => {
    authService.logout();
    setUser(null);
  };

  const updateUser = (userData: Partial<User>) => {
    if (user) {
      const updatedUser = { ...user, ...userData };
      setUser(updatedUser);
      localStorage.setItem('user', JSON.stringify(updatedUser));
    }
  };

  const value: AuthContextType = {
    user,
    loading,
    login,
    register,
    logout,
    updateUser
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};