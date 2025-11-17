import React, { createContext, ReactNode, useContext, useEffect, useState } from 'react';
import { useAuthService } from '../services/api';
import { User } from '../types/index';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (usernameOrEmail: string, password: string) => Promise<{ success: boolean; error?: string }>;
  register: (username: string, email: string, password: string) => Promise<{ success: boolean; error?: string }>;
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

  // Get the API service hooks inside the component
  const { login: apiLogin, register: apiRegister, logout: apiLogout, getCurrentUser } = useAuthService();

  // Only run initializeAuth once on mount, not on every render
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
            const currentUser = await getCurrentUser();
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
    // eslint-disable-next-line
  }, []);

  const login = async (usernameOrEmail: string, password: string): Promise<{ success: boolean; error?: string }> => {
    try {
      console.log('🔐 AuthContext: Starting login process');
      console.log('📧 Username/Email:', usernameOrEmail);
      console.log('🔑 Password:', password ? '***provided***' : 'NOT PROVIDED');

      const response = await apiLogin({ usernameOrEmail, password });

      console.log('📡 AuthService response:', response);

      if (response.success && response.data) {
        console.log('✅ Login successful, setting user:', response.data.user);
        // Persist token and user for authenticated requests
        try {
          localStorage.setItem('auth_token', response.data.token);
          localStorage.setItem('user', JSON.stringify(response.data.user));
        } catch (_) {}
        setUser(response.data.user);
        return { success: true };
      } else {
        console.log('❌ Login failed:', response.error || 'Unknown error');
        return { success: false, error: response.error || 'Login failed' };
      }
    } catch (error) {
      console.error('❌ Login exception:', error);
      return { success: false, error: 'Login failed. Please try again.' };
    }
  };

  const register = async (username: string, email: string, password: string): Promise<{ success: boolean; error?: string }> => {
    try {
      console.log('AuthContext: Starting registration process');
      console.log('Username:', username);
      console.log('Email:', email);
      console.log('Password:', password ? '***provided***' : 'NOT PROVIDED');

      const response = await apiRegister({
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
        return { success: true };
      } else {
        console.log('Registration failed:', response.error || 'Unknown error');
        return { success: false, error: response.error || 'Registration failed' };
      }
    } catch (error) {
      console.error('Registration exception:', error);
      return { success: false, error: 'Registration failed. Please try again.' };
    }
  };

  const logout = () => {
    apiLogout();
    setUser(null);
    try {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user');
    } catch (_) {}
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
