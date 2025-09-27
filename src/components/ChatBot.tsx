import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  MessageCircle, 
  Send, 
  Trash2, 
  Bot, 
  User, 
  Loader2,
  AlertTriangle,
  Shield,
  Clock,
  Lightbulb
} from 'lucide-react';
import { chatbotService, ChatMessage, ChatResponse } from '../services/chatbotService';

interface ChatBotProps {
  className?: string;
  initialMessage?: string;
}

const ChatBot: React.FC<ChatBotProps> = ({ className = '', initialMessage = '' }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState(initialMessage);
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [error, setError] = useState('');
  const [userName, setUserName] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  // Load conversation history on component mount
  useEffect(() => {
    loadConversationHistory();
  }, []);

  // Set initial message if provided
  useEffect(() => {
    if (initialMessage && initialMessage.trim()) {
      setInputMessage(initialMessage);
    }
  }, [initialMessage]);

  const loadConversationHistory = async () => {
    try {
      const response = await chatbotService.getConversationHistory();
      if (response.success && response.data) {
        setMessages(response.data.conversation);
        setUserName(response.data.user_name);
      }
    } catch (error) {
      console.error('Failed to load conversation history:', error);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    setError('');
    setIsLoading(true);
    setIsTyping(true);

    // Add user message immediately
    const newUserMessage: ChatMessage = {
      message: userMessage,
      sender: 'user',
      timestamp: new Date().toISOString()
    };
    setMessages(prev => [...prev, newUserMessage]);

    try {
      const response: ChatResponse = await chatbotService.sendMessage(userMessage, true);
      
      if (response.success && response.data) {
        // Add bot response
        const botMessage: ChatMessage = {
          message: response.data.bot_response,
          sender: 'bot',
          timestamp: response.data.timestamp
        };
        
        setMessages(prev => [...prev, botMessage]);
        
        // Set user name if we got it
        if (!userName && response.data.spam_analysis) {
          // We can get user name from the response or keep it from history
        }
      } else {
        setError(response.error || 'Failed to send message');
      }
    } catch (error) {
      setError('Failed to send message. Please try again.');
      console.error('Chat error:', error);
    } finally {
      setIsLoading(false);
      setIsTyping(false);
    }
  };

  const clearConversation = async () => {
    try {
      const response = await chatbotService.clearConversation();
      if (response.success) {
        setMessages([]);
        setError('');
      } else {
        setError(response.error || 'Failed to clear conversation');
      }
    } catch (error) {
      setError('Failed to clear conversation');
      console.error('Clear conversation error:', error);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const MessageBubble: React.FC<{ message: ChatMessage; index: number }> = ({ message, index }) => {
    const isUser = message.sender === 'user';
    const timestamp = chatbotService.formatTimestamp(message.timestamp);

    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: index * 0.1 }}
        className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}
      >
        <div className={`flex items-start space-x-2 max-w-[80%] ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
          {/* Avatar */}
          <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
            isUser 
              ? 'bg-blue-500 text-white' 
              : 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
          }`}>
            {isUser ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
          </div>

          {/* Message Content */}
          <div className={`rounded-2xl px-4 py-3 ${
            isUser 
              ? 'bg-blue-500 text-white rounded-br-md' 
              : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white rounded-bl-md'
          }`}>
            <div className="whitespace-pre-wrap text-sm leading-relaxed">
              {message.message}
            </div>
            {timestamp && (
              <div className={`text-xs mt-1 ${
                isUser ? 'text-blue-100' : 'text-gray-500 dark:text-gray-400'
              }`}>
                {timestamp}
              </div>
            )}
          </div>
        </div>
      </motion.div>
    );
  };

  const TypingIndicator: React.FC = () => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="flex justify-start mb-4"
    >
      <div className="flex items-start space-x-2 max-w-[80%]">
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 text-white flex items-center justify-center">
          <Bot className="h-4 w-4" />
        </div>
        <div className="bg-gray-100 dark:bg-gray-700 rounded-2xl rounded-bl-md px-4 py-3">
          <div className="flex space-x-1">
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
          </div>
        </div>
      </div>
    </motion.div>
  );

  return (
    <div className={`flex flex-col h-full bg-white dark:bg-gray-800 rounded-lg shadow-lg ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-t-lg">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center">
            <MessageCircle className="h-5 w-5" />
          </div>
          <div>
            <h3 className="font-semibold">AI Assistant</h3>
            <p className="text-sm text-purple-100">
              {userName ? `Chatting with ${userName}` : 'Ready to help with SMS analysis'}
            </p>
          </div>
        </div>
        
        {messages.length > 0 && (
          <button
            onClick={clearConversation}
            className="p-2 hover:bg-white/20 rounded-lg transition-colors"
            title="Clear conversation"
          >
            <Trash2 className="h-4 w-4" />
          </button>
        )}
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 min-h-0">
        {messages.length === 0 && !isTyping && (
          <div className="text-center py-8">
            <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
              <Bot className="h-8 w-8 text-white" />
            </div>
            <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Hi there! 👋
            </h4>
            <p className="text-gray-600 dark:text-gray-400 max-w-sm mx-auto">
              I'm your AI assistant for SMS spam detection. Send me any suspicious message and I'll help you understand if it's safe or not!
            </p>
          </div>
        )}

        {messages.map((message, index) => (
          <MessageBubble key={index} message={message} index={index} />
        ))}

        <AnimatePresence>
          {isTyping && <TypingIndicator />}
        </AnimatePresence>

        <div ref={messagesEndRef} />
      </div>

      {/* Error Display */}
      {error && (
        <div className="px-4 py-2 bg-red-50 dark:bg-red-900/20 border-t border-red-200 dark:border-red-800">
          <div className="flex items-center space-x-2 text-red-600 dark:text-red-400">
            <AlertTriangle className="h-4 w-4" />
            <span className="text-sm">{error}</span>
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="p-4 border-t border-gray-200 dark:border-gray-700">
        <div className="flex space-x-2">
          <div className="flex-1 relative">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Type your message or paste a suspicious SMS here..."
              className="w-full px-4 py-3 pr-12 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 resize-none"
              rows={1}
              style={{ minHeight: '48px', maxHeight: '120px' }}
              disabled={isLoading}
            />
          </div>
          <button
            onClick={sendMessage}
            disabled={!inputMessage.trim() || isLoading}
            className="px-4 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg hover:from-purple-600 hover:to-pink-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center justify-center min-w-[48px]"
          >
            {isLoading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
          </button>
        </div>
        
        <div className="mt-2 text-xs text-gray-500 dark:text-gray-400 text-center">
          Press Enter to send • Shift+Enter for new line
        </div>
      </div>
    </div>
  );
};

export default ChatBot;
