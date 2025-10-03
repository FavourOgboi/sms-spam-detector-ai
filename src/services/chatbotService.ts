/**
 * Simple chatbot service for SMS spam detection help
 */

import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "https://sms-guard-backend.onrender.com/api";

export interface ChatMessage {
  id: string;
  text: string;
  sender: "user" | "bot";
  timestamp: Date;
}

export interface ChatResponse {
  success: boolean;
  data?: {
    response: string;
    user: string;
  };
  error?: string;
}

export interface SuggestionsResponse {
  success: boolean;
  data?: {
    suggestions: string[];
  };
  error?: string;
}

/**
 * Send a message to the chatbot
 */
export const sendMessage = async (
  message: string,
  context?: { message?: string; prediction?: any }
): Promise<ChatResponse> => {
  try {
    const token = localStorage.getItem("auth_token");

    if (!token) {
      throw new Error("Not authenticated");
    }

    const payload: any = { message };
    if (context) {
      if (context.message) payload.contextMessage = context.message;
      if (context.prediction) payload.contextPrediction = context.prediction;
    }

    const response = await axios.post(
      `${API_URL}/chatbot/chat`,
      payload,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }
    );

    return response.data;
  } catch (error: any) {
    if (error.response?.data) {
      return error.response.data;
    }
    return {
      success: false,
      error: error.message || "Failed to send message",
    };
  }
};

/**
 * Get suggested questions
 */
export const getSuggestions = async (): Promise<SuggestionsResponse> => {
  try {
    const token = localStorage.getItem("auth_token");

    if (!token) {
      throw new Error("Not authenticated");
    }

    const response = await axios.get(`${API_URL}/chatbot/suggestions`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    return response.data;
  } catch (error: any) {
    if (error.response?.data) {
      return error.response.data;
    }
    return {
      success: false,
      error: error.message || "Failed to get suggestions",
    };
  }
};

/**
 * Generate a unique ID for messages
 */
export const generateMessageId = (): string => {
  return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
};
