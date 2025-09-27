import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  MessageCircle, 
  Bot, 
  Shield, 
  Lightbulb, 
  AlertTriangle,
  CheckCircle,
  Info,
  Zap
} from 'lucide-react';
import ChatBot from '../components/ChatBot';
import { chatbotService } from '../services/chatbotService';

const Chat: React.FC = () => {
  const [quickAnalysisMessage, setQuickAnalysisMessage] = useState('');
  const [quickAnalysisResult, setQuickAnalysisResult] = useState<any>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleQuickAnalysis = async () => {
    if (!quickAnalysisMessage.trim()) return;

    setIsAnalyzing(true);
    try {
      const result = await chatbotService.quickAnalyze(quickAnalysisMessage);
      setQuickAnalysisResult(result);
    } catch (error) {
      console.error('Quick analysis error:', error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const exampleMessages = [
    "Your account is expiring. Verify your information to continue service: [link]",
    "Congratulations! You've won $1000! Click here to claim your prize!",
    "Hi, how are you doing today?",
    "URGENT! Your bank account has been compromised. Click immediately!",
    "Meeting scheduled for 3pm in conference room B"
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-pink-50 dark:from-gray-900 dark:via-gray-800 dark:to-purple-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <div className="flex items-center justify-center mb-4">
            <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mr-4">
              <MessageCircle className="h-8 w-8 text-white" />
            </div>
            <div>
              <h1 className="text-4xl font-bold text-gray-900 dark:text-white">
                AI Chat Assistant
              </h1>
              <p className="text-lg text-gray-600 dark:text-gray-300 mt-2">
                Get personalized help with SMS spam detection
              </p>
            </div>
          </div>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Chat Area */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="lg:col-span-2"
          >
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl overflow-hidden" style={{ height: '600px' }}>
              <ChatBot className="h-full" />
            </div>
          </motion.div>

          {/* Sidebar */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
            className="space-y-6"
          >
            {/* Features Card */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <Bot className="h-5 w-5 mr-2 text-purple-500" />
                AI Features
              </h3>
              <div className="space-y-3">
                <div className="flex items-start space-x-3">
                  <Shield className="h-5 w-5 text-green-500 mt-0.5" />
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white">Spam Detection</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Analyzes messages using your trained AI model
                    </p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <Lightbulb className="h-5 w-5 text-yellow-500 mt-0.5" />
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white">Smart Explanations</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Shows why messages are flagged as spam
                    </p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <CheckCircle className="h-5 w-5 text-blue-500 mt-0.5" />
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white">Personalized Advice</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Tailored recommendations for your situation
                    </p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <Zap className="h-5 w-5 text-purple-500 mt-0.5" />
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white">Context Aware</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Understands conversation and message context
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Quick Examples */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <Info className="h-5 w-5 mr-2 text-blue-500" />
                Try These Examples
              </h3>
              <div className="space-y-2">
                {exampleMessages.slice(0, 3).map((message, index) => (
                  <button
                    key={index}
                    onClick={() => setQuickAnalysisMessage(message)}
                    className="w-full text-left p-3 rounded-lg bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors text-sm text-gray-700 dark:text-gray-300"
                  >
                    "{message.length > 60 ? message.substring(0, 60) + '...' : message}"
                  </button>
                ))}
              </div>
            </div>

            {/* Safety Tips */}
            <div className="bg-gradient-to-r from-red-50 to-orange-50 dark:from-red-900/20 dark:to-orange-900/20 rounded-2xl shadow-lg p-6 border border-red-200 dark:border-red-800">
              <h3 className="text-xl font-semibold text-red-800 dark:text-red-300 mb-4 flex items-center">
                <AlertTriangle className="h-5 w-5 mr-2" />
                Safety Tips
              </h3>
              <div className="space-y-2 text-sm text-red-700 dark:text-red-300">
                <p>• Never click suspicious links</p>
                <p>• Don't share personal information</p>
                <p>• Verify with official sources</p>
                <p>• Trust your instincts</p>
                <p>• When in doubt, delete and block</p>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Quick Analysis Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="mt-8"
        >
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6">
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <Zap className="h-5 w-5 mr-2 text-yellow-500" />
              Quick Analysis
            </h3>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Get instant AI analysis of any message without starting a full conversation.
            </p>
            
            <div className="flex space-x-4">
              <div className="flex-1">
                <textarea
                  value={quickAnalysisMessage}
                  onChange={(e) => setQuickAnalysisMessage(e.target.value)}
                  placeholder="Paste a suspicious message here for quick analysis..."
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 resize-none"
                  rows={3}
                />
              </div>
              <button
                onClick={handleQuickAnalysis}
                disabled={!quickAnalysisMessage.trim() || isAnalyzing}
                className="px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg hover:from-purple-600 hover:to-pink-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center justify-center min-w-[120px]"
              >
                {isAnalyzing ? (
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                ) : (
                  'Analyze'
                )}
              </button>
            </div>

            {quickAnalysisResult && quickAnalysisResult.success && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-6 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg"
              >
                <div className="whitespace-pre-wrap text-gray-800 dark:text-gray-200">
                  {quickAnalysisResult.data.advice}
                </div>
              </motion.div>
            )}
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Chat;
