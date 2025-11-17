import axios from 'axios';

const API_URL = "https://sms-spam-detector-ai-production.up.railway.app/api";

export const usePredictionService = () => {
  const predictSpam = async (data) => {
    const response = await axios.post(`${API_URL}/predict`, data);
    return response.data;
  };

  const explainPrediction = async (predictionId) => {
    const response = await axios.get(`${API_URL}/predictions/${predictionId}/explain`);
    return response.data;
  };

  const getAllPredictions = async () => {
    const response = await axios.get(`${API_URL}/predictions`);
    return response.data;
  };

  return {
    predictSpam,
    explainPrediction,
    getAllPredictions,
  };
};

export const useUserService = () => {
  const getUserStats = async () => {
    const response = await axios.get(`${API_URL}/user/stats`);
    return response.data;
  };

  const updateUserProfile = async (profileData) => {
    const response = await axios.put(`${API_URL}/user/profile`, profileData);
    return response.data;
  };

  const getPredictionHistory = async (page = 1, perPage = 10) => {
    const response = await axios.get(`${API_URL}/predictions/history?page=${page}&per_page=${perPage}`);
    return response.data;
  };

  const getUserPredictions = async (userId) => {
    const response = await axios.get(`${API_URL}/user/${userId}/predictions`);
    return response.data;
  };

  return {
    getUserStats,
    updateUserProfile,
    getPredictionHistory,
    getUserPredictions,
  };
};

export const useAuthService = () => {
  const login = async (loginData) => {
    const response = await axios.post(`${API_URL}/auth/login`, loginData);
    return response.data;
  };

  const register = async (registerData) => {
    const response = await axios.post(`${API_URL}/auth/register`, registerData);
    return response.data;
  };

  const logout = async () => {
    const response = await axios.post(`${API_URL}/auth/logout`);
    return response.data;
  };

  const getCurrentUser = async () => {
    const response = await axios.get(`${API_URL}/auth/me`);
    return response.data;
  };

  const forgotPassword = async (data) => {
    const response = await axios.post(`${API_URL}/forgot-password`, data);
    return response.data;
  };

  const resetPassword = async (data) => {
    const response = await axios.post(`${API_URL}/reset-password`, data);
    return response.data;
  };

  return {
    login,
    register,
    logout,
    getCurrentUser,
    forgotPassword,
    resetPassword,
  };
};

export default API_URL;
