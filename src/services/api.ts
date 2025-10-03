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


const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://sms-guard-backend.onrender.com/api';

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
    // Backend expects 'Bearer token_' format
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Add response interceptor to handle common errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle 401 errors globally
    if (error.response?.status === 401) {
      // Token expired or invalid, clear storage
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user');
      localStorage.removeItem('predictions');

      // Redirect to login if not already there
      if (window.location.pathname !== '/login' && window.location.pathname !== '/register') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// Utility functions
export const isAuthenticated = (): boolean => {
  const token = localStorage.getItem('auth_token');
  const user = localStorage.getItem('user');
  return !!(token && user);
};

export const getCurrentUserFromStorage = (): User | null => {
  try {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  } catch {
    return null;
  }
};

// Authentication Services
export const authService = {
  // Flask /api/auth/login endpoint
  async login(credentials: AuthCredentials): Promise<ApiResponse<AuthResponse>> {
    try {
      console.log('🌐 API Service: Making login request');
      console.log('📤 Request URL:', `${API_BASE_URL}/auth/login`);
      console.log('📤 Request data:', {
        usernameOrEmail: credentials.usernameOrEmail,
        password: credentials.password ? '***provided***' : 'NOT PROVIDED'
      });

      const response = await api.post('/auth/login', {
        usernameOrEmail: credentials.usernameOrEmail,
        password: credentials.password
      });

      console.log('📥 Response status:', response.status);
      console.log('📥 Response data:', response.data);

      if (response.data.success) {
        const { token, user } = response.data.data;
        localStorage.setItem('auth_token', token);
        localStorage.setItem('user', JSON.stringify(user));

        console.log('✅ Login successful, token stored');
        return {
          success: true,
          data: { token, user }
        };
      } else {
        console.log('❌ Login failed from server:', response.data.error);
        return {
          success: false,
          error: response.data.error || 'Login failed'
        };
      }
    } catch (error: any) {
      console.error('❌ API Login error:', error);
      console.error('❌ Error response:', error.response?.data);
      console.error('❌ Error status:', error.response?.status);

      const errorMessage = error.response?.data?.error || 'Login failed. Please try again.';
      return {
        success: false,
        error: errorMessage
      };
    }
  },

  // Flask /api/auth/register endpoint
  async register(credentials: RegisterCredentials): Promise<ApiResponse<AuthResponse>> {
    console.log('=== FRONTEND REGISTRATION START ===');
    console.log('API_BASE_URL:', API_BASE_URL);
    console.log('Full URL:', `${API_BASE_URL}/auth/register`);
    console.log('Credentials:', {
      username: credentials.username,
      email: credentials.email,
      password: credentials.password ? '***provided***' : 'NOT PROVIDED'
    });

    try {
      const requestData = {
        username: credentials.username,
        email: credentials.email,
        password: credentials.password
      };

      console.log('Making POST request...');
      const response = await api.post('/auth/register', requestData);

      console.log('Response received:', response.status, response.data);

      if (response.data.success) {
        const { token, user } = response.data.data;
        localStorage.setItem('auth_token', token);
        localStorage.setItem('user', JSON.stringify(user));

        console.log('Registration successful!');
        return {
          success: true,
          data: { token, user }
        };
      } else {
        console.log('Registration failed:', response.data.error);
        return {
          success: false,
          error: response.data.error || 'Registration failed'
        };
      }
    } catch (error: any) {
      console.error('Registration request failed:', error);
      console.error('Error details:', {
        message: error.message,
        status: error.response?.status,
        data: error.response?.data,
        url: error.config?.url
      });

      const errorMessage = error.response?.data?.error || 'Network error. Please try again.';
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
  },

  // Flask /api/auth/forgot-password endpoint
  async forgotPassword(email: string): Promise<ApiResponse<{ message: string; resetLink?: string; debug?: boolean }>> {
    try {
      console.log('🔄 API Service: Making forgot password request');
      console.log('📤 Email:', email);

      const response = await api.post('/auth/forgot-password', {
        email: email.trim().toLowerCase()
      });

      console.log('📥 Forgot password response:', response.data);

      if (response.data.success) {
        return {
          success: true,
          data: {
            message: response.data.message,
            resetLink: response.data.resetLink, // For development mode
            debug: response.data.debug
          }
        };
      } else {
        return {
          success: false,
          error: response.data.error || 'Failed to send reset link'
        };
      }
    } catch (error: any) {
      console.error('❌ Forgot password error:', error);
      const errorMessage = error.response?.data?.error || 'Network error. Please try again.';
      return {
        success: false,
        error: errorMessage
      };
    }
  },

  // Flask /api/auth/reset-password endpoint
  async resetPassword(token: string, newPassword: string, userId?: string): Promise<ApiResponse<{ message: string }>> {
    try {
      console.log('🔄 API Service: Making reset password request');
      console.log('📤 Token:', token.substring(0, 20) + '...');
      console.log('📤 User ID:', userId);

      const requestData: any = {
        token: token,
        password: newPassword
      };

      // Add user_id if provided
      if (userId) {
        requestData.user_id = userId;
      }

      const response = await api.post('/auth/reset-password', requestData);

      console.log('📥 Reset password response:', response.data);

      if (response.data.success) {
        return {
          success: true,
          data: {
            message: response.data.message || 'Password reset successful'
          }
        };
      } else {
        return {
          success: false,
          error: response.data.error || 'Failed to reset password'
        };
      }
    } catch (error: any) {
      console.error('❌ Reset password error:', error);
      const errorMessage = error.response?.data?.error || 'Network error. Please try again.';
      return {
        success: false,
        error: errorMessage
      };
    }
  }

};

// Prediction Services
export const predictionService = {
  // Flask /api/predict endpoint
  // Updated: expects EnsemblePredictionResult from backend
  async predictSpam(message: string): Promise<ApiResponse<import('../types').EnsemblePredictionResult>> {
    try {
      console.log('🔮 API Service: Making prediction request');
      console.log('📤 Message length:', message.length);

      if (!message.trim()) {
        return {
          success: false,
          error: 'Message cannot be empty'
        };
      }

      const response = await api.post('/predict', {
        message: message.trim()
      });

      console.log('📥 Prediction response status:', response.status);
      console.log('📥 Prediction response data:', response.data);

      if (response.data.success) {
        const predictionData = response.data.data;

        // Validate ensemble prediction data structure
        if (!predictionData.consensus || !predictionData.model_results) {
          console.warn('⚠️  Invalid ensemble prediction data structure:', predictionData);
        }

        return {
          success: true,
          data: predictionData
        };
      } else {
        console.error('❌ Prediction failed from server:', response.data.error);
        return {
          success: false,
          error: response.data.error || 'Prediction failed'
        };
      }
    } catch (error: any) {
      console.error('❌ Prediction API error:', error);
      console.error('❌ Error response:', error.response?.data);

      const errorMessage = error.response?.data?.error || 'Prediction failed. Please try again.';
      return {
        success: false,
        error: errorMessage
      };
    }
  },

  // Dedicated explanation endpoint
  async explainPrediction(message: string, numFeatures: number = 10): Promise<ApiResponse<any>> {
    try {
      console.log('🔍 API Service: Getting detailed explanation');
      console.log('📤 Request data:', { message: message.substring(0, 50) + '...', numFeatures });

      // Use the dedicated explain endpoint
      const response = await api.post('/explain', {
        message: message,
        num_features: numFeatures
      });

      console.log('📥 Explanation response:', response.data);

      if (response.data.success) {
        return {
          success: true,
          data: response.data.data
        };
      } else {
        return {
          success: false,
          error: response.data.error || 'Explanation failed'
        };
      }
    } catch (error: any) {
      console.error('❌ Explanation error:', error);
      // console.error('Error details:', error.response?.data);
      console.error('Full error object:', error);
      const errorMessage = error.response?.data?.error || 'Unable to explain prediction. Please try again.';
      return {
        success: false,
        error: errorMessage
      };
    }
  }
};

export const getModelMetrics = async () => {
  try {
    const response = await api.get('/model/metrics');
    if (response.data.success) {
      return { success: true, data: response.data.data };
    } else {
      return { success: false, error: response.data.error || 'Failed to fetch model metrics' };
    }
  } catch (error: any) {
    return { success: false, error: error.response?.data?.error || 'Failed to fetch model metrics.' };
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
  async changePassword(passwordData: { currentPassword: string; newPassword: string; confirmNewPassword?: string }): Promise<ApiResponse<void>> {
    try {
      console.log('PASSWORD CHANGE: Starting request');
      console.log('PASSWORD CHANGE: Data:', {
        currentPassword: passwordData.currentPassword ? '***provided***' : 'EMPTY',
        newPassword: passwordData.newPassword ? '***provided***' : 'EMPTY',
        confirmNewPassword: passwordData.confirmNewPassword ? '***provided***' : 'EMPTY'
      });

      const requestData = {
        currentPassword: passwordData.currentPassword,
        newPassword: passwordData.newPassword,
        confirmNewPassword: passwordData.confirmNewPassword || passwordData.newPassword
      };

      const response = await api.put('/user/change-password', requestData);
      console.log('PASSWORD CHANGE: Response:', response.status, response.data);

      if (response.data.success) {
        console.log('PASSWORD CHANGE: Success');
        return {
          success: true
        };
      } else {
        console.log('PASSWORD CHANGE: Failed:', response.data.error);
        return {
          success: false,
          error: response.data.error || 'Failed to change password'
        };
      }
    } catch (error: any) {
      console.error('PASSWORD CHANGE: Error:', error);
      console.error('PASSWORD CHANGE: Error response:', error.response?.data);
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
