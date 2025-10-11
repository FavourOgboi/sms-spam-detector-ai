import axios from "axios";
import { useApiUrl } from "../contexts/ApiUrlContext";
import {
  ApiResponse,
  AuthCredentials,
  AuthResponse,
  PredictionResult,
  RegisterCredentials,
  User,
  UserStats,
} from "../types/index";

// Custom hook to get an axios instance with the current API URL
export const useApi = () => {
  const { apiUrl } = useApiUrl();

  const api = axios.create({
    baseURL: apiUrl,
    headers: {
      "Content-Type": "application/json",
    },
  });

  // Add token interceptor for authenticated requests
  api.interceptors.request.use((config) => {
    const token = localStorage.getItem("auth_token");
    if (token && config.headers) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    // Debug: log outgoing request headers
    console.log("API Request Headers:", config.headers);
    return config;
  });

  // Add response interceptor to handle common errors
  api.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401) {
        // Only log out if the request is NOT to /api/predict or /api/explain
        const url = error.config?.url || "";
        if (
          !url.includes("/api/predict") &&
          !url.includes("/api/explain")
        ) {
          localStorage.removeItem("auth_token");
          localStorage.removeItem("user");
          localStorage.removeItem("predictions");
          if (
            window.location.pathname !== "/login" &&
            window.location.pathname !== "/register"
          ) {
            window.location.href = "/login";
          }
        }
      }
      return Promise.reject(error);
    }
  );

  return api;
};

// Authentication Services
export const useAuthService = () => {
  const api = useApi();

  return {
    async login(
      credentials: AuthCredentials
    ): Promise<ApiResponse<AuthResponse>> {
      try {
  const response = await api.post("/auth/login", {
          usernameOrEmail: credentials.usernameOrEmail,
          password: credentials.password,
        });

        if (response.data.success) {
          const { token, user } = response.data.data;
          localStorage.setItem("auth_token", token);
          localStorage.setItem("user", JSON.stringify(user));
          return {
            success: true,
            data: { token, user },
          };
        } else {
          return {
            success: false,
            error: response.data.error || "Login failed",
          };
        }
      } catch (error: any) {
        const errorMessage =
          error.response?.data?.error || "Login failed. Please try again.";
        return {
          success: false,
          error: errorMessage,
        };
      }
    },

    async register(
      credentials: RegisterCredentials
    ): Promise<ApiResponse<AuthResponse>> {
      try {
        const requestData = {
          username: credentials.username,
          email: credentials.email,
          password: credentials.password,
        };
  const response = await api.post("/auth/register", requestData);

        if (response.data.success) {
          const { token, user } = response.data.data;
          localStorage.setItem("auth_token", token);
          localStorage.setItem("user", JSON.stringify(user));
          return {
            success: true,
            data: { token, user },
          };
        } else {
          return {
            success: false,
            error: response.data.error || "Registration failed",
          };
        }
      } catch (error: any) {
        const errorMessage =
          error.response?.data?.error || "Network error. Please try again.";
        return {
          success: false,
          error: errorMessage,
        };
      }
    },

    async logout(): Promise<void> {
      localStorage.removeItem("auth_token");
      localStorage.removeItem("user");
      localStorage.removeItem("predictions");
    },

    async getCurrentUser(): Promise<User | null> {
      try {
        const token = localStorage.getItem("auth_token");
        if (!token) {
          return null;
        }
        const response = await api.get("/api/auth/me");
        if (response.data.success) {
          const user = response.data.data;
          localStorage.setItem("user", JSON.stringify(user));
          return user;
        } else {
          localStorage.removeItem("auth_token");
          localStorage.removeItem("user");
          return null;
        }
      } catch (error) {
        localStorage.removeItem("auth_token");
        localStorage.removeItem("user");
        return null;
      }
    },

    async forgotPassword(
      email: string
    ): Promise<ApiResponse<{ message: string; resetLink?: string; debug?: boolean }>> {
      try {
        const response = await api.post("/auth/forgot-password", {
          email: email.trim().toLowerCase(),
        });
        if (response.data.success) {
          return {
            success: true,
            data: {
              message: response.data.message,
              resetLink: response.data.resetLink,
              debug: response.data.debug,
            },
          };
        } else {
          return {
            success: false,
            error: response.data.error || "Failed to send reset link",
          };
        }
      } catch (error: any) {
        const errorMessage =
          error.response?.data?.error || "Network error. Please try again.";
        return {
          success: false,
          error: errorMessage,
        };
      }
    },

    async resetPassword(
      token: string,
      newPassword: string,
      userId?: string
    ): Promise<ApiResponse<{ message: string }>> {
      try {
        const requestData: any = {
          token: token,
          password: newPassword,
        };
        if (userId) {
          requestData.user_id = userId;
        }
        const response = await api.post("/auth/reset-password", requestData);
        if (response.data.success) {
          return {
            success: true,
            data: {
              message: response.data.message || "Password reset successful",
            },
          };
        } else {
          return {
            success: false,
            error: response.data.error || "Failed to reset password",
          };
        }
      } catch (error: any) {
        const errorMessage =
          error.response?.data?.error || "Network error. Please try again.";
        return {
          success: false,
          error: errorMessage,
        };
      }
    },
  };
};

// Prediction Services
export const usePredictionService = () => {
  const api = useApi();

  return {
    async predictSpam(
      message: string
    ): Promise<ApiResponse<import("../types").EnsemblePredictionResult>> {
      try {
        if (!message.trim()) {
          return {
            success: false,
            error: "Message cannot be empty",
          };
        }
  const response = await api.post("/predict", {
          message: message.trim(),
        });
        if (response.data.success) {
          const predictionData = response.data.data;
          return {
            success: true,
            data: predictionData,
          };
        } else {
          return {
            success: false,
            error: response.data.error || "Prediction failed",
          };
        }
      } catch (error: any) {
        const errorMessage =
          error.response?.data?.error || "Prediction failed. Please try again.";
        return {
          success: false,
          error: errorMessage,
        };
      }
    },

    async explainPrediction(
      message: string,
      numFeatures: number = 10
    ): Promise<ApiResponse<any>> {
      try {
  const response = await api.post("/explain", {
          message: message,
          num_features: numFeatures,
        });
        if (response.data.success) {
          return {
            success: true,
            data: response.data.data,
          };
        } else {
          return {
            success: false,
            error: response.data.error || "Explanation failed",
          };
        }
      } catch (error: any) {
        const errorMessage =
          error.response?.data?.error ||
          "Unable to explain prediction. Please try again.";
        return {
          success: false,
          error: errorMessage,
        };
      }
    },
  };
};

export const useUserService = () => {
  const api = useApi();

  return {
    async getUserStats(): Promise<ApiResponse<UserStats>> {
      try {
  const response = await api.get("/user/stats");
        if (response.data.success) {
          return {
            success: true,
            data: response.data.data,
          };
        } else {
          return {
            success: false,
            error: response.data.error || "Failed to fetch user statistics",
          };
        }
      } catch (error: any) {
        const errorMessage =
          error.response?.data?.error || "Failed to fetch user statistics.";
        return {
          success: false,
          error: errorMessage,
        };
      }
    },

    async getUserPredictions(): Promise<ApiResponse<PredictionResult[]>> {
      try {
  const response = await api.get("/user/predictions");
        if (response.data.success) {
          return {
            success: true,
            data: response.data.data,
          };
        } else {
          return {
            success: false,
            error: response.data.error || "Failed to fetch predictions",
          };
        }
      } catch (error: any) {
        const errorMessage =
          error.response?.data?.error || "Failed to fetch predictions.";
        return {
          success: false,
          error: errorMessage,
        };
      }
    },

    async updateProfile(
      profileData: Partial<User>,
      profileImage?: File | null
    ): Promise<ApiResponse<User>> {
      try {
        let response;
        if (profileImage) {
          const formData = new FormData();
          Object.keys(profileData).forEach((key) => {
            const value = profileData[key as keyof User];
            if (value !== undefined) {
              formData.append(key, String(value));
            }
          });
          formData.append("profileImage", profileImage);
          response = await api.put("/user/profile", formData, {
            headers: { "Content-Type": "multipart/form-data" },
          });
        } else {
          response = await api.put("/user/profile", profileData);
        }
        if (response.data.success) {
          let updatedUser = response.data.data;
          // Fix: If profile_image URL is http://localhost:5000, rewrite to 8080
          if (updatedUser && updatedUser.profile_image && typeof updatedUser.profile_image === "string") {
            updatedUser.profile_image = updatedUser.profile_image.replace("http://localhost:5000", "http://localhost:8080");
          }
          localStorage.setItem("user", JSON.stringify(updatedUser));
          return {
            success: true,
            data: updatedUser,
          };
        } else {
          return {
            success: false,
            error: response.data.error || "Failed to update profile",
          };
        }
      } catch (error: any) {
        const errorMessage =
          error.response?.data?.error || "Failed to update profile.";
        return {
          success: false,
          error: errorMessage,
        };
      }
    },

    async changePassword(passwordData: {
      currentPassword: string;
      newPassword: string;
      confirmNewPassword?: string;
    }): Promise<ApiResponse<void>> {
      try {
        const requestData = {
          currentPassword: passwordData.currentPassword,
          newPassword: passwordData.newPassword,
          confirmNewPassword:
            passwordData.confirmNewPassword || passwordData.newPassword,
        };
  const response = await api.put("/user/change-password", requestData);
        if (response.data.success) {
          return {
            success: true,
          };
        } else {
          return {
            success: false,
            error: response.data.error || "Failed to change password",
          };
        }
      } catch (error: any) {
        const errorMessage =
          error.response?.data?.error || "Failed to change password.";
        return {
          success: false,
          error: errorMessage,
        };
      }
    },

    async deleteAccount(): Promise<ApiResponse<void>> {
      try {
  const response = await api.delete("/user/delete");
        if (response.data.success) {
          localStorage.removeItem("auth_token");
          localStorage.removeItem("user");
          return {
            success: true,
          };
        } else {
          return {
            success: false,
            error: response.data.error || "Failed to delete account",
          };
        }
      } catch (error: any) {
        const errorMessage =
          error.response?.data?.error || "Failed to delete account.";
        return {
          success: false,
          error: errorMessage,
        };
      }
    },
  };
};
