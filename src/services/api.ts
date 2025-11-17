import axios, { AxiosInstance } from 'axios';
import { AuthResponse, PredictionResult, User, UserStats } from '../types';

const API_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8080/api";

// ---- Demo Mode Helpers ----
export const isDemoModeActive = (): boolean => {
  try {
    const flag = import.meta.env.VITE_DEMO_MODE === 'true';
    const stored = localStorage.getItem('demo_mode') === 'true';
    return !!(flag || stored);
  } catch (_) {
    return import.meta.env.VITE_DEMO_MODE === 'true';
  }
};

export const DEMO_USER: User = {
  id: 'demo-user',
  username: 'demo',
  email: 'demo@sms-guard.app',
  profileImage: undefined,
  bio: 'Demo account for presentations',
  memberSince: new Date(2024, 0, 1).toISOString(),
  isAuthenticated: true,
  theme: 'light'
};

const DEMO_TOKEN = 'demo-token';
const DEMO_HISTORY_KEY = 'demo_predictions';

// Utilities for demo data persistence
const loadDemoHistory = (): PredictionResult[] => {
  try {
    return JSON.parse(localStorage.getItem(DEMO_HISTORY_KEY) || '[]');
  } catch {
    return [];
  }
};

const saveDemoHistory = (items: PredictionResult[]) => {
  try { localStorage.setItem(DEMO_HISTORY_KEY, JSON.stringify(items)); } catch {}
};

// Simple heuristic to mock predictions
const scoreSpam = (message: string): number => {
  const spamWords = ['win', 'prize', 'lottery', 'free', 'click', 'link', 'claim', 'urgent', 'money', 'credit', 'offer'];
  const hamWords = ['hello', 'hi', 'meeting', 'lunch', 'tomorrow', 'thanks', 'please'];
  const m = message.toLowerCase();
  let score = 0.1;
  spamWords.forEach(w => { if (m.includes(w)) score += 0.15; });
  hamWords.forEach(w => { if (m.includes(w)) score -= 0.08; });
  score += Math.min(0.2, (message.length - 80) / 400); // longer msgs slightly more ham
  return Math.max(0.02, Math.min(0.98, score));
};

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
    if (isDemoModeActive()) {
      const data: { success: boolean; data: AuthResponse } = {
        success: true,
        data: { token: DEMO_TOKEN, user: DEMO_USER }
      };
      return data;
    }
    const res = await axios.post(`${API_URL}/auth/login`, payload);
    return res.data;
  };

  const register = async (payload: { username: string; email: string; password: string; }) => {
    if (isDemoModeActive()) {
      return { success: true, message: 'Demo mode: registration simulated' };
    }
    const res = await axios.post(`${API_URL}/auth/register`, payload);
    return res.data;
  };

  const logout = async () => {
    if (isDemoModeActive()) {
      return { success: true };
    }
    const res = await http.post(`/auth/logout`);
    return res.data;
  };

  const getCurrentUser = async () => {
    if (isDemoModeActive()) {
      return DEMO_USER; // mimic backend returning user in data
    }
    const res = await http.get(`/auth/me`);
    // Backend returns { success, data: user }
    return res.data?.data;
  };

  const forgotPassword = async (email: string) => {
    if (isDemoModeActive()) {
      return { success: true, message: 'Demo mode: password reset link simulated' };
    }
    const res = await axios.post(`${API_URL}/auth/forgot-password`, { email });
    return res.data;
  };

  const resetPassword = async (token: string, password: string) => {
    if (isDemoModeActive()) {
      return { success: true, message: 'Demo mode: password reset simulated' };
    }
    const res = await axios.post(`${API_URL}/auth/reset-password`, { token, password });
    return res.data;
  };

  return { login, register, logout, getCurrentUser, forgotPassword, resetPassword };
};

// User related API
export const useUserService = () => {
  const getUserStats = async () => {
    if (isDemoModeActive()) {
      const history = loadDemoHistory();
      const spamCount = history.filter(h => h.prediction === 'spam').length;
      const hamCount = history.filter(h => h.prediction === 'ham').length;
      const total = history.length;
      const avgConfidence = total ? history.reduce((s, h) => s + (h.confidence || 0), 0) / total : 0.92;
      const stats: UserStats = {
        totalMessages: total,
        spamCount,
        hamCount,
        accuracy: 0.955,
        spamRate: total ? spamCount / total : 0.32,
        avgConfidence,
        recentPredictions: history.slice(-10).reverse(),
        accuracyData: { validationAccuracy: 0.955, realTimeAccuracy: total >= 10 ? 0.94 : undefined }
      };
      return { success: true, data: stats };
    }
    const res = await http.get(`/user/stats`);
    return res.data; // { success, data }
  };

  const updateUserProfile = async (profileData: Record<string, any>) => {
    if (isDemoModeActive()) {
      // Persist to localStorage user for demo
      try {
        const userRaw = localStorage.getItem('user');
        if (userRaw) {
          const u = { ...JSON.parse(userRaw), ...profileData };
          localStorage.setItem('user', JSON.stringify(u));
        }
      } catch {}
      return { success: true, message: 'Demo mode: profile updated locally' };
    }
    const res = await http.put(`/user/profile`, profileData);
    return res.data;
  };

  const getPredictionHistory = async (page: number = 1, perPage: number = 10) => {
    if (isDemoModeActive()) {
      const history = loadDemoHistory();
      const start = (page - 1) * perPage;
      const end = start + perPage;
      return { success: true, data: history.slice(start, end) };
    }
    const res = await http.get(`/user/predictions`, { params: { page, per_page: perPage } });
    return res.data;
  };

  const getUserPredictions = async (page: number = 1, perPage: number = 50) => {
    if (isDemoModeActive()) {
      const history = loadDemoHistory();
      const start = (page - 1) * perPage;
      const end = start + perPage;
      return { success: true, data: history.slice(start, end) };
    }
    const res = await http.get(`/user/predictions`, { params: { page, per_page: perPage } });
    return res.data;
  };

  return { getUserStats, updateUserProfile, getPredictionHistory, getUserPredictions };
};

// Prediction related API
export const usePredictionService = () => {
  const predictSpam = async (message: string) => {
    if (isDemoModeActive()) {
      const spamProb = scoreSpam(message);
      const hamProb = 1 - spamProb;
      const now = new Date().toISOString();

      const mkRes = (pred: 'spam' | 'ham', conf: number): PredictionResult => ({
        id: `demo_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`,
        message,
        prediction: pred,
        confidence: conf,
        spamProbability: spamProb,
        hamProbability: hamProb,
        timestamp: now,
        userId: DEMO_USER.id,
      });

      const nb = mkRes(spamProb > 0.55 ? 'spam' : 'ham', Math.max(spamProb, hamProb) * 0.96);
      const svm = mkRes(spamProb > 0.6 ? 'spam' : 'ham', Math.max(spamProb, hamProb) * 0.93);
      const lr = mkRes(spamProb > 0.5 ? 'spam' : 'ham', Math.max(spamProb, hamProb) * 0.90);

      const model_results: Record<string, PredictionResult> = {
        'Naive Bayes': nb,
        'SVM': svm,
        'Logistic Regression': lr,
      };

      const spamVotes = [nb, svm, lr].filter(r => r.prediction === 'spam').length;
      const hamVotes = 3 - spamVotes;
      const majority_vote = spamVotes > hamVotes ? 'spam' : 'ham';

      const data = {
        success: true,
        data: {
          consensus: {
            majority_vote,
            weighted_vote: majority_vote,
            confidence: Math.max(nb.confidence, svm.confidence, lr.confidence),
            majority_count: Math.max(spamVotes, hamVotes),
            total_votes: 3,
            spam_votes: spamVotes,
            ham_votes: hamVotes,
            model_count: 3,
          },
          model_results,
          weighted_result: {
            weighted_spam_prob: spamProb,
            weighted_majority: majority_vote as 'spam' | 'ham' | 'unknown'
          },
          confidence_level: Math.max(nb.confidence, svm.confidence, lr.confidence) > 0.85 ? 'High' : 'Medium',
          suggestion: majority_vote === 'spam' ? 'Be cautious. Do not click links or share info.' : 'Message looks safe.',
          message,
        }
      };

      // Save to demo history
      const history = loadDemoHistory();
      history.push({ ...model_results['Naive Bayes'] });
      saveDemoHistory(history);

      return data;
    }

    const res = await http.post(`/predict`, { message });
    return res.data;
  };

  const explainPrediction = async (message: string, numFeatures: number = 10) => {
    if (isDemoModeActive()) {
      const words = message.toLowerCase().split(/\W+/).filter(Boolean);
      const counts: Record<string, number> = {};
      words.forEach(w => counts[w] = (counts[w] || 0) + 1);
      const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, numFeatures);
      return {
        success: true,
        data: {
          method: 'demo-top-words',
          summary: 'Top contributing words based on frequency (demo).',
          top_features: sorted.map(([w, c]) => ({
            feature: w,
            importance: Math.min(1, c / (words.length || 1)),
            direction: ['win','prize','free','click','claim','urgent'].includes(w) ? 'spam' : 'ham'
          }))
        }
      };
    }

    const res = await http.post(`/explain`, { message, num_features: numFeatures });
    return res.data;
  };

  const getAllPredictions = async (page: number = 1, perPage: number = 50) => {
    if (isDemoModeActive()) {
      const history = loadDemoHistory();
      const start = (page - 1) * perPage;
      const end = start + perPage;
      return { success: true, data: history.slice(start, end) };
    }
    const res = await http.get(`/user/predictions`, { params: { page, per_page: perPage } });
    return res.data;
  };

  return { predictSpam, explainPrediction, getAllPredictions };
};

export default API_URL;
