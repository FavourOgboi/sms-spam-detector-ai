import axios from 'axios';
import { 
  User, 
  AuthCredentials, 
  RegisterCredentials, 
  PredictionResult, 
  UserStats, 
  ApiResponse, 
  AuthResponse 
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
  // TODO: Connect to Flask /api/auth/login endpoint
  // Expected request: POST /api/auth/login with { usernameOrEmail: string, password: string }
  // Expected response: { success: boolean, data: { token: string, user: User }, error?: string }
  async login(credentials: AuthCredentials): Promise<ApiResponse<AuthResponse>> {
    try {
      // Mock implementation - replace with actual API call
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate network delay
      
      // Demo credentials for development testing only - remove in production
      if ((credentials.usernameOrEmail === 'demo' || credentials.usernameOrEmail === 'demo@example.com') && credentials.password === 'demo123') {
        const mockUser: User = {
          id: 'demo-user-id',
          username: 'Demo User',
          email: 'demo@example.com',
          profileImage: undefined, // No profile image initially
          bio: 'Professional user of SMS Guard spam detection system',
          memberSince: '2024-01-15',
          isAuthenticated: true,
          theme: 'light'
        };
        
        const token = 'mock_jwt_token_' + Date.now();
        localStorage.setItem('auth_token', token);
        localStorage.setItem('user', JSON.stringify(mockUser));
        
        return {
          success: true,
          data: { token, user: mockUser }
        };
      }
      
      return {
        success: false,
        error: 'Invalid credentials'
      };
    } catch (error) {
      return {
        success: false,
        error: 'Login failed. Please try again.'
      };
    }
  },

  // TODO: Connect to Flask /api/auth/register endpoint
  // Expected request: POST /api/auth/register with { username: string, email: string, password: string }
  // Expected response: { success: boolean, data: { token: string, user: User }, error?: string }
  async register(credentials: RegisterCredentials): Promise<ApiResponse<AuthResponse>> {
    try {
      // Mock implementation - replace with actual API call
      await new Promise(resolve => setTimeout(resolve, 1200));
      
      const mockUser: User = {
        id: Math.random().toString(36).substr(2, 9),
        username: credentials.username,
        email: credentials.email,
        profileImage: '/pres.jpg',
        bio: '',
        memberSince: new Date().toISOString().split('T')[0],
        isAuthenticated: true,
        theme: 'light'
      };
      
      const token = 'mock_jwt_token_' + Date.now();
      localStorage.setItem('auth_token', token);
      localStorage.setItem('user', JSON.stringify(mockUser));
      
      return {
        success: true,
        data: { token, user: mockUser }
      };
    } catch (error) {
      return {
        success: false,
        error: 'Registration failed. Please try again.'
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

  // TODO: Connect to Flask /api/auth/me endpoint
  // Expected request: GET /api/auth/me with Authorization header
  // Expected response: { success: boolean, data: User, error?: string }
  async getCurrentUser(): Promise<User | null> {
    try {
      const userStr = localStorage.getItem('user');
      if (userStr) {
        return JSON.parse(userStr);
      }
      return null;
    } catch {
      return null;
    }
  }
};

// Prediction Services
export const predictionService = {
  // TODO: Connect to Flask /api/predict endpoint
  // Expected request: POST /api/predict with { message: string }
  // Expected response: { success: boolean, data: PredictionResult, error?: string }
  async predictSpam(message: string): Promise<ApiResponse<PredictionResult>> {
    try {
      await new Promise(resolve => setTimeout(resolve, 2000)); // Simulate ML processing time
      
      // Mock prediction logic - replace with actual API call
      const spamKeywords = ['free', 'winner', 'urgent', 'limited time', 'click now', 'congratulations', 'prize', 'claim', 'offer'];
      const messageWords = message.toLowerCase().split(' ');
      const spamScore = spamKeywords.filter(keyword => 
        messageWords.some(word => word.includes(keyword))
      ).length;
      
      const isSpam = spamScore > 0 || Math.random() > 0.7;
      const confidence = Math.random() * 0.3 + (isSpam ? 0.7 : 0.8);
      
      const currentUser = JSON.parse(localStorage.getItem('user') || '{}');
      const result: PredictionResult = {
        id: Math.random().toString(36).substr(2, 9),
        message,
        prediction: isSpam ? 'spam' : 'ham',
        confidence: Math.round(confidence * 100) / 100,
        timestamp: new Date().toISOString(),
        userId: currentUser.id || 'unknown'
      };
      
      // Store prediction with user isolation
      const userPredictionsKey = `predictions_${currentUser.id}`;
      const existingPredictions = JSON.parse(localStorage.getItem(userPredictionsKey) || '[]');
      existingPredictions.unshift(result);
      localStorage.setItem(userPredictionsKey, JSON.stringify(existingPredictions.slice(0, 100)));
      
      return {
        success: true,
        data: result
      };
    } catch (error) {
      return {
        success: false,
        error: 'Prediction failed. Please try again.'
      };
    }
  }
};

// User Services
export const userService = {
  // TODO: Connect to Flask /api/user/stats endpoint
  // Expected request: GET /api/user/stats with Authorization header
  // Expected response: { success: boolean, data: UserStats, error?: string }
  async getUserStats(): Promise<ApiResponse<UserStats>> {
    try {
      await new Promise(resolve => setTimeout(resolve, 800));
      
      const currentUser = JSON.parse(localStorage.getItem('user') || '{}');
      const userPredictionsKey = `predictions_${currentUser.id}`;
      const predictions: PredictionResult[] = JSON.parse(localStorage.getItem(userPredictionsKey) || '[]');
      
      const spamCount = predictions.filter(p => p.prediction === 'spam').length;
      const hamCount = predictions.filter(p => p.prediction === 'ham').length;
      const totalMessages = predictions.length;
      
      const spamRate = totalMessages > 0 ? spamCount / totalMessages : 0;
      const avgConfidence = totalMessages > 0 
        ? predictions.reduce((sum, p) => sum + p.confidence, 0) / totalMessages 
        : 0;
      
      const stats: UserStats = {
        totalMessages,
        spamCount,
        hamCount,
        accuracy: Math.round((Math.random() * 0.1 + 0.9) * 100) / 100, // Mock accuracy
        spamRate: Math.round(spamRate * 100) / 100,
        avgConfidence: Math.round(avgConfidence * 100) / 100,
        recentPredictions: predictions.slice(0, 10)
      };
      
      return {
        success: true,
        data: stats
      };
    } catch (error) {
      return {
        success: false,
        error: 'Failed to fetch user statistics.'
      };
    }
  },

  // TODO: Connect to Flask /api/user/predictions endpoint
  // Expected request: GET /api/user/predictions with Authorization header
  // Expected response: { success: boolean, data: PredictionResult[], error?: string }
  async getUserPredictions(): Promise<ApiResponse<PredictionResult[]>> {
    try {
      await new Promise(resolve => setTimeout(resolve, 600));
      
      const currentUser = JSON.parse(localStorage.getItem('user') || '{}');
      const userPredictionsKey = `predictions_${currentUser.id}`;
      const predictions: PredictionResult[] = JSON.parse(localStorage.getItem(userPredictionsKey) || '[]');
      
      return {
        success: true,
        data: predictions
      };
    } catch (error) {
      return {
        success: false,
        error: 'Failed to fetch predictions.'
      };
    }
  },

  // TODO: Connect to Flask /api/user/profile endpoint
  // Expected request: PUT /api/user/profile with Authorization header and profile data
  // Expected response: { success: boolean, data: User, error?: string }
  async updateProfile(profileData: Partial<User>, profileImage?: File | null): Promise<ApiResponse<User>> {
    try {
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // TODO: In real implementation, handle file upload here
      // const formData = new FormData();
      // Object.keys(profileData).forEach(key => {
      //   formData.append(key, profileData[key]);
      // });
      // if (profileImage) {
      //   formData.append('profileImage', profileImage);
      // }
      // const response = await api.put('/user/profile', formData, {
      //   headers: { 'Content-Type': 'multipart/form-data' }
      // });
      
      const currentUser = JSON.parse(localStorage.getItem('user') || '{}');
      const updatedUser = { ...currentUser, ...profileData };
      localStorage.setItem('user', JSON.stringify(updatedUser));
      
      return {
        success: true,
        data: updatedUser
      };
    } catch (error) {
      return {
        success: false,
        error: 'Failed to update profile.'
      };
    }
  },

  // TODO: Connect to Flask /api/user/change-password endpoint
  // Expected request: PUT /api/user/change-password with Authorization header and password data
  // Expected response: { success: boolean, error?: string }
  async changePassword(passwordData: { currentPassword: string; newPassword: string; confirmNewPassword: string }): Promise<ApiResponse<void>> {
    try {
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Mock validation - in real implementation, backend would verify current password
      if (passwordData.currentPassword !== 'demo123') {
        return {
          success: false,
          error: 'Current password is incorrect'
        };
      }
      
      if (passwordData.newPassword.length < 6) {
        return {
          success: false,
          error: 'New password must be at least 6 characters long'
        };
      }
      
      if (passwordData.newPassword !== passwordData.confirmNewPassword) {
        return {
          success: false,
          error: 'New passwords do not match'
        };
      }
      
      // In real implementation, this would update the password in the database
      return {
        success: true
      };
    } catch (error) {
      return {
        success: false,
        error: 'Failed to change password.'
      };
    }
  },

  // TODO: Connect to Flask /api/user/delete endpoint
  // Expected request: DELETE /api/user/delete with Authorization header
  // Expected response: { success: boolean, error?: string }
  async deleteAccount(): Promise<ApiResponse<void>> {
    try {
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      const currentUser = JSON.parse(localStorage.getItem('user') || '{}');
      const userPredictionsKey = `predictions_${currentUser.id}`;
      
      // Clear all user data with proper isolation
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user');
      localStorage.removeItem(userPredictionsKey);
      
      return {
        success: true
      };
    } catch (error) {
      return {
        success: false,
        error: 'Failed to delete account.'
      };
    }
  }
};

export default api;