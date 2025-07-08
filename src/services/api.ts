import axios from 'axios';
import {
    ApiResponse,
    AuthCredentials,
    AuthResponse,
    PredictionResult,
    RegisterCredentials,
    User,
    UserStats
} from '../types/index';

// TODO: Replace with actual Flask backend URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token interceptor for authenticated requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Authentication Services
export const authService = {
  // Flask /api/auth/login endpoint
  async login(credentials: AuthCredentials): Promise<ApiResponse<AuthResponse>> {
    try {
      const response = await api.post('/auth/login', {
        usernameOrEmail: credentials.usernameOrEmail,
        password: credentials.password
      });

      if (response.data.success) {
        const { token, user } = response.data.data;
        localStorage.setItem('auth_token', token);
        localStorage.setItem('user', JSON.stringify(user));

        return {
          success: true,
          data: { token, user }
        };
      } else {
        return {
          success: false,
          error: response.data.error || 'Login failed'
        };
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || 'Login failed. Please try again.';
      return {
        success: false,
        error: errorMessage
      };
    }
  },

  // Flask /api/auth/register endpoint
  async register(credentials: RegisterCredentials): Promise<ApiResponse<AuthResponse>> {
    try {
      const response = await api.post('/auth/register', {
        username: credentials.username,
        email: credentials.email,
        password: credentials.password
      });

      if (response.data.success) {
        const { token, user } = response.data.data;
        localStorage.setItem('auth_token', token);
        localStorage.setItem('user', JSON.stringify(user));

        return {
          success: true,
          data: { token, user }
        };
      } else {
        return {
          success: false,
          error: response.data.error || 'Registration failed'
        };
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || 'Registration failed. Please try again.';
      return {
        success: false,
        error: errorMessage
      };
    }
  },

  // TODO: Connect to Flask /api/auth/logout endpoint
  // Expected request: POST /api/auth/logout with Authorization header
  // Expected response: { success: boolean }
  async logout(): Promise<void> {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
    // Clear user-specific data to ensure data isolation
    localStorage.removeItem('predictions');
  },

  // Flask /api/auth/me endpoint
  async getCurrentUser(): Promise<User | null> {
    try {
      const token = localStorage.getItem('auth_token');
      if (!token) {
        return null;
      }

      const response = await api.get('/auth/me');

      if (response.data.success) {
        const user = response.data.data;
        localStorage.setItem('user', JSON.stringify(user));
        return user;
      } else {
        // Token might be invalid, clear storage
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user');
        return null;
      }
    } catch (error) {
      // Token might be invalid, clear storage
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user');
      return null;
    }
  }
};

// Prediction Services
export const predictionService = {
  // Flask /api/predict endpoint
  async predictSpam(message: string): Promise<ApiResponse<PredictionResult>> {
    try {
      const response = await api.post('/predict', {
        message: message
      });

      if (response.data.success) {
        return {
          success: true,
          data: response.data.data
        };
      } else {
        return {
          success: false,
          error: response.data.error || 'Prediction failed'
        };
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || 'Prediction failed. Please try again.';
      return {
        success: false,
        error: errorMessage
      };
    }
  }
};

// User Services
export const userService = {
  // Flask /api/user/stats endpoint
  async getUserStats(): Promise<ApiResponse<UserStats>> {
    try {
      const response = await api.get('/user/stats');

      if (response.data.success) {
        return {
          success: true,
          data: response.data.data
        };
      } else {
        return {
          success: false,
          error: response.data.error || 'Failed to fetch user statistics'
        };
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || 'Failed to fetch user statistics.';
      return {
        success: false,
        error: errorMessage
      };
    }
  },

  // Flask /api/user/predictions endpoint
  async getUserPredictions(): Promise<ApiResponse<PredictionResult[]>> {
    try {
      const response = await api.get('/user/predictions');

      if (response.data.success) {
        return {
          success: true,
          data: response.data.data
        };
      } else {
        return {
          success: false,
          error: response.data.error || 'Failed to fetch predictions'
        };
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || 'Failed to fetch predictions.';
      return {
        success: false,
        error: errorMessage
      };
    }
  },

  // Flask /api/user/profile endpoint
  async updateProfile(profileData: Partial<User>, profileImage?: File | null): Promise<ApiResponse<User>> {
    try {
      let response;

      if (profileImage) {
        // Handle file upload with FormData
        const formData = new FormData();
        Object.keys(profileData).forEach(key => {
          const value = profileData[key as keyof User];
          if (value !== undefined) {
            formData.append(key, String(value));
          }
        });
        formData.append('profileImage', profileImage);

        response = await api.put('/user/profile', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
      } else {
        // Regular JSON update
        response = await api.put('/user/profile', profileData);
      }

      if (response.data.success) {
        const updatedUser = response.data.data;
        localStorage.setItem('user', JSON.stringify(updatedUser));

        return {
          success: true,
          data: updatedUser
        };
      } else {
        return {
          success: false,
          error: response.data.error || 'Failed to update profile'
        };
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || 'Failed to update profile.';
      return {
        success: false,
        error: errorMessage
      };
    }
  },

  // Flask /api/user/change-password endpoint
  async changePassword(passwordData: { currentPassword: string; newPassword: string; confirmNewPassword: string }): Promise<ApiResponse<void>> {
    try {
      const response = await api.put('/user/change-password', {
        currentPassword: passwordData.currentPassword,
        newPassword: passwordData.newPassword,
        confirmNewPassword: passwordData.confirmNewPassword
      });

      if (response.data.success) {
        return {
          success: true
        };
      } else {
        return {
          success: false,
          error: response.data.error || 'Failed to change password'
        };
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || 'Failed to change password.';
      return {
        success: false,
        error: errorMessage
      };
    }
  },

  // Flask /api/user/delete endpoint
  async deleteAccount(): Promise<ApiResponse<void>> {
    try {
      const response = await api.delete('/user/delete');

      if (response.data.success) {
        // Clear local storage after successful deletion
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user');

        return {
          success: true
        };
      } else {
        return {
          success: false,
          error: response.data.error || 'Failed to delete account'
        };
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || 'Failed to delete account.';
      return {
        success: false,
        error: errorMessage
      };
    }
  }
};

export default api;