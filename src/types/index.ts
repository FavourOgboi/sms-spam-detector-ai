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
  contribution?: number;
  present: boolean;
  explanation: string;
  method?: 'LIME' | 'SHAP' | 'COMBINED' | 'KEYWORD';
  methods?: string[];
}

export interface PredictionResult {
  id: string;
  message: string;
  prediction: 'spam' | 'ham';
  confidence: number;
  spamProbability?: number;
  hamProbability?: number;
  modelName?: string;
  modelVersion?: string;
  processingTimeMs?: number;
  featureCount?: number;
  topFeatures?: ExplanationFeature[];
  timestamp: string;
  userId: string;
}

export interface AccuracyData {
  trainingAccuracy: number;
  validationAccuracy: number;
  realTimeAccuracy: number | null;
}

export interface UserStats {
  totalMessages: number;
  spamCount: number;
  hamCount: number;
  accuracy?: number; // Keep for backward compatibility
  accuracyData?: AccuracyData; // New enhanced accuracy data
  spamRate: number;
  avgConfidence: number;
  avgProcessingTime?: number; // New field
  modelStats?: any; // New field
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