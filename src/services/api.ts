import axios from 'axios';

const API_URL = "https://sms-spam-detector-ai-production.up.railway.app/api";

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
