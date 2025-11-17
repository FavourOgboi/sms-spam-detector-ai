/**
 * Simple chatbot service for SMS spam detection help
 */

import axios from "axios";
import API_URL, { isDemoModeActive } from "./api";

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
    // Demo mode: return a simulated helpful reply without backend
    if (isDemoModeActive()) {
      const base = "This is a demo response. In a full setup, the chatbot would analyze your message and context.";
      const tip = /http|www\.|bit\.ly|link|click/i.test(message)
        ? "Tip: Avoid clicking shortened or unknown links."
        : "Tip: Legitimate messages rarely pressure you to act immediately.";
      const response = `${base}\n\nYou said: "${message}"\n${tip}`;
      return { success: true, data: { response, user: 'demo' } };
    }

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
    if (isDemoModeActive()) {
      return {
        success: true,
        data: {
          suggestions: [
            "How do I know if a message is spam?",
            "Is this link safe to click?",
            "What should I do with suspicious messages?",
          ],
        },
      };
    }

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
