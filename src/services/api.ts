import axios, { AxiosInstance } from 'axios';

const API_URL = "https://sms-spam-detector-ai-production.up.railway.app/api";

// Axios instance that automatically attaches JWT token
const http: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

http.interceptors.request.use((config) => {
  try {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers = config.headers || {};
      (config.headers as any).Authorization = `Bearer ${token}`;
    }
  } catch (_) {
    // ignore SSR/localStorage errors
  }
  return config;
});

// Auth related API
export const useAuthService = () => {
  const login = async (payload: { usernameOrEmail: string; password: string; }) => {
    const res = await axios.post(`${API_URL}/auth/login`, payload);
    return res.data;
  };

  const register = async (payload: { username: string; email: string; password: string; }) => {
    const res = await axios.post(`${API_URL}/auth/register`, payload);
    return res.data;
  };

  const logout = async () => {
    const res = await http.post(`/auth/logout`);
    return res.data;
  };

  const getCurrentUser = async () => {
    const res = await http.get(`/auth/me`);
    // Backend returns { success, data: user }
    return res.data?.data;
  };

  const forgotPassword = async (email: string) => {
    const res = await axios.post(`${API_URL}/auth/forgot-password`, { email });
    return res.data;
  };

  const resetPassword = async (token: string, password: string) => {
    const res = await axios.post(`${API_URL}/auth/reset-password`, { token, password });
    return res.data;
  };

  return { login, register, logout, getCurrentUser, forgotPassword, resetPassword };
};

// User related API
export const useUserService = () => {
  const getUserStats = async () => {
    const res = await http.get(`/user/stats`);
    return res.data; // { success, data }
  };

  const updateUserProfile = async (profileData: Record<string, any>) => {
    const res = await http.put(`/user/profile`, profileData);
    return res.data;
  };

  const getPredictionHistory = async (page: number = 1, perPage: number = 10) => {
    const res = await http.get(`/user/predictions`, { params: { page, per_page: perPage } });
    return res.data;
  };

  const getUserPredictions = async (page: number = 1, perPage: number = 50) => {
    const res = await http.get(`/user/predictions`, { params: { page, per_page: perPage } });
    return res.data;
  };

  return { getUserStats, updateUserProfile, getPredictionHistory, getUserPredictions };
};

// Prediction related API
export const usePredictionService = () => {
  const predictSpam = async (message: string) => {
    const res = await http.post(`/predict`, { message });
    return res.data;
  };

  const explainPrediction = async (message: string, numFeatures: number = 10) => {
    const res = await http.post(`/explain`, { message, num_features: numFeatures });
    return res.data;
  };

  const getAllPredictions = async (page: number = 1, perPage: number = 50) => {
    const res = await http.get(`/user/predictions`, { params: { page, per_page: perPage } });
    return res.data;
  };

  return { predictSpam, explainPrediction, getAllPredictions };
};

export default API_URL;
