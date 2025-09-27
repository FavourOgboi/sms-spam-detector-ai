/**
 * Chatbot Service
 * 
 * Handles communication with the AI chatbot API for conversational
 * assistance with SMS spam detection and user guidance.
 */

import { apiClient } from './api';

export interface ChatMessage {
  message: string;
  sender: 'user' | 'bot';
  timestamp: string;
}

export interface SpamAnalysis {
  prediction: string;
  confidence: number;
  model_version: string;
  processing_time_ms: number;
}

export interface ExplanationFeature {
  feature: string;
  importance: number;
  direction: 'spam' | 'ham';
  tf_idf_score?: number;
  frequency?: number;
}

export interface Explanation {
  success: boolean;
  method: string;
  summary: string;
  features: ExplanationFeature[];
  spam_indicators?: ExplanationFeature[];
  ham_indicators?: ExplanationFeature[];
}

export interface ChatResponse {
  success: boolean;
  data?: {
    bot_response: string;
    user_message: string;
    timestamp: string;
    spam_analysis?: SpamAnalysis;
    explanation?: Explanation;
    conversation_length: number;
    processing_time_ms: number;
  };
  error?: string;
}

export interface ConversationHistory {
  success: boolean;
  data?: {
    conversation: ChatMessage[];
    summary: {
      has_conversation: boolean;
      total_messages: number;
      user_messages: number;
      bot_messages: number;
      conversation_start?: string;
      last_message?: string;
    };
    user_name: string;
  };
  error?: string;
}

export interface QuickAnalysis {
  success: boolean;
  data?: {
    message: string;
    advice: string;
    context_analysis: {
      detected_scenario?: string;
      scenario_confidence: number;
      suspicious_elements: string[];
      message_length: number;
      has_numbers: boolean;
      has_caps: boolean;
    };
    spam_prediction?: SpamAnalysis;
    explanation?: Explanation;
    user_name: string;
  };
  error?: string;
}

export interface SpamScenarios {
  success: boolean;
  data?: {
    scenarios: Record<string, {
      name: string;
      keywords: string[];
      advice: string;
    }>;
    total_scenarios: number;
  };
  error?: string;
}

class ChatbotService {
  /**
   * Send a message to the AI chatbot
   */
  async sendMessage(message: string, analyzeMessage: boolean = true): Promise<ChatResponse> {
    try {
      const response = await apiClient.post('/chatbot/chat', {
        message: message.trim(),
        analyze_message: analyzeMessage
      });

      return {
        success: true,
        data: response.data.data
      };
    } catch (error: any) {
      console.error('Chat error:', error);
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to send message'
      };
    }
  }

  /**
   * Get conversation history
   */
  async getConversationHistory(): Promise<ConversationHistory> {
    try {
      const response = await apiClient.get('/chatbot/conversation');

      return {
        success: true,
        data: response.data.data
      };
    } catch (error: any) {
      console.error('Get conversation error:', error);
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to get conversation history'
      };
    }
  }

  /**
   * Clear conversation history
   */
  async clearConversation(): Promise<{ success: boolean; message?: string; error?: string }> {
    try {
      const response = await apiClient.post('/chatbot/clear');

      return {
        success: true,
        message: response.data.message
      };
    } catch (error: any) {
      console.error('Clear conversation error:', error);
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to clear conversation'
      };
    }
  }

  /**
   * Quick analyze a message without full conversation
   */
  async quickAnalyze(message: string): Promise<QuickAnalysis> {
    try {
      const response = await apiClient.post('/chatbot/quick-analyze', {
        message: message.trim()
      });

      return {
        success: true,
        data: response.data.data
      };
    } catch (error: any) {
      console.error('Quick analyze error:', error);
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to analyze message'
      };
    }
  }

  /**
   * Get spam scenarios information
   */
  async getSpamScenarios(): Promise<SpamScenarios> {
    try {
      const response = await apiClient.get('/chatbot/scenarios');

      return {
        success: true,
        data: response.data.data
      };
    } catch (error: any) {
      console.error('Get scenarios error:', error);
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to get spam scenarios'
      };
    }
  }

  /**
   * Format timestamp for display
   */
  formatTimestamp(timestamp: string): string {
    try {
      const date = new Date(timestamp);
      return date.toLocaleTimeString([], { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: true 
      });
    } catch {
      return '';
    }
  }

  /**
   * Format date for display
   */
  formatDate(timestamp: string): string {
    try {
      const date = new Date(timestamp);
      const today = new Date();
      const yesterday = new Date(today);
      yesterday.setDate(yesterday.getDate() - 1);

      if (date.toDateString() === today.toDateString()) {
        return 'Today';
      } else if (date.toDateString() === yesterday.toDateString()) {
        return 'Yesterday';
      } else {
        return date.toLocaleDateString([], { 
          month: 'short', 
          day: 'numeric',
          year: date.getFullYear() !== today.getFullYear() ? 'numeric' : undefined
        });
      }
    } catch {
      return '';
    }
  }

  /**
   * Get confidence level description
   */
  getConfidenceDescription(confidence: number): string {
    if (confidence >= 0.9) return 'Very High';
    if (confidence >= 0.7) return 'High';
    if (confidence >= 0.5) return 'Medium';
    if (confidence >= 0.3) return 'Low';
    return 'Very Low';
  }

  /**
   * Get prediction color class
   */
  getPredictionColor(prediction: string): string {
    return prediction.toLowerCase() === 'spam' 
      ? 'text-red-600 dark:text-red-400' 
      : 'text-green-600 dark:text-green-400';
  }

  /**
   * Get confidence color class
   */
  getConfidenceColor(confidence: number): string {
    if (confidence >= 0.8) return 'text-green-600 dark:text-green-400';
    if (confidence >= 0.6) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-red-600 dark:text-red-400';
  }
}

// Export singleton instance
export const chatbotService = new ChatbotService();
