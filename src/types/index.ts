export interface User {
  id: string;
  username: string;
  email: string;
  profileImage?: string;
  bio?: string;
  memberSince: string;
  isAuthenticated: boolean;
  theme?: 'light' | 'dark';
}

export interface AuthCredentials {
  usernameOrEmail: string;
  password: string;
}

export interface RegisterCredentials {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
}

export interface PasswordChangeData {
  currentPassword: string;
  newPassword: string;
  confirmNewPassword: string;
}

export interface ExplanationFeature {
  feature: string;
  importance: number;
  direction: 'spam' | 'ham';
  abs_importance?: number;
  frequency?: number;
}

export interface BasicExplanation {
  method: string;
  summary: string;
  top_features: ExplanationFeature[];
}

export interface PredictionResult {
  id: string;
  message: string;
  prediction: 'spam' | 'ham';
  confidence: number;
  spamProbability?: number;
  hamProbability?: number;
  topFeatures?: ExplanationFeature[];
  explanation?: BasicExplanation;
  timestamp: string;
  userId: string;
}

export interface UserStats {
  totalMessages: number;
  spamCount: number;
  hamCount: number;
  accuracy: number;
  spamRate: number;
  avgConfidence: number;
  recentPredictions: PredictionResult[];
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

export interface AuthResponse {
  token: string;
  user: User;
}

export interface ChartData {
  name: string;
  value: number;
  color: string;
}

export interface ThemeContextType {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}