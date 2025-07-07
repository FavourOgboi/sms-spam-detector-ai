import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { MessageSquare, Send, AlertTriangle, CheckCircle, BarChart3, History, Lightbulb } from 'lucide-react';
import { Link } from 'react-router-dom';
import { predictionService } from '../services/api';
import { PredictionResult } from '../types/index';
import LoadingSpinner from '../components/ui/LoadingSpinner';
import GuardAnimation from '../components/ui/GuardAnimation';

const Predict: React.FC = () => {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim()) {
      setError('SMS message cannot be empty');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await predictionService.predictSpam(message);
      if (response.success && response.data) {
        setResult(response.data);
      } else {
        setError(response.error || 'Prediction failed');
      }
    } catch (err) {
      setError('Prediction failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setMessage('');
    setResult(null);
    setError('');
  };

  const isFormValid = message.trim().length > 0;

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">SMS Spam Detection</h1>
        <p className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
          Analyze your SMS messages using our advanced machine learning model. 
          Simply paste your message below and get instant spam detection results.
        </p>
      </motion.div>

      {/* Guard Animation - Only show when analyzing */}
      {loading && (
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          className="flex justify-center"
        >
          <GuardAnimation isAnalyzing={loading} />
        </motion.div>
      )}

      {/* Main Form */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 p-8"
      >
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="message" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
              Enter SMS Message
            </label>
            <textarea
              id="message"
              value={message}
              onChange={(e) => {
                setMessage(e.target.value);
                if (error) setError(''); // Clear error when user starts typing
              }}
              className="w-full h-32 px-4 py-3 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none transition-all duration-200"
              placeholder="Paste your SMS message here to check if it's spam..."
              maxLength={500}
              disabled={loading}
            />
            <div className="flex justify-between items-center mt-2">
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Maximum 500 characters
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                {message.length}/500
              </p>
            </div>
          </div>

          {error && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 px-4 py-3 rounded-lg"
            >
              {error}
            </motion.div>
          )}

          <div className="flex space-x-4">
            <motion.button
              type="submit"
              disabled={!isFormValid || loading}
              whileHover={{ scale: loading ? 1 : 1.02 }}
              whileTap={{ scale: loading ? 1 : 0.98 }}
              className="flex-1 bg-primary-500 text-white py-3 px-6 rounded-lg font-medium hover:bg-primary-600 focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
            >
              {loading ? (
                <div className="flex items-center justify-center">
                  <LoadingSpinner size="sm" className="mr-2" />
                  Analyzing...
                </div>
              ) : (
                <div className="flex items-center justify-center">
                  <Send className="h-5 w-5 mr-2" />
                  Analyze Message
                </div>
              )}
            </motion.button>

            {(result || error) && (
              <motion.button
                type="button"
                onClick={resetForm}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="px-6 py-3 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 rounded-lg font-medium hover:bg-gray-50 dark:hover:bg-gray-600 transition-all duration-200"
              >
                Reset
              </motion.button>
            )}
          </div>
        </form>
      </motion.div>

      {/* Results */}
      {result && (
        <motion.div
          initial={{ opacity: 0, y: 20, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ delay: 0.1 }}
          className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 overflow-hidden"
        >
          <div className={`px-8 py-6 ${
            result.prediction === 'spam' 
              ? 'bg-gradient-to-r from-red-50 to-red-100 dark:from-red-900/20 dark:to-red-800/20 border-b-2 border-red-200 dark:border-red-800' 
              : 'bg-gradient-to-r from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20 border-b-2 border-green-200 dark:border-green-800'
          }`}>
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                {result.prediction === 'spam' ? (
                  <AlertTriangle className="h-8 w-8 text-red-500" />
                ) : (
                  <CheckCircle className="h-8 w-8 text-green-500" />
                )}
                <div>
                  <h3 className="text-2xl font-bold text-gray-900 dark:text-white">
                    {result.prediction === 'spam' ? 'SPAM DETECTED' : 'SAFE MESSAGE'}
                  </h3>
                  <p className={`text-sm ${
                    result.prediction === 'spam' ? 'text-red-700 dark:text-red-300' : 'text-green-700 dark:text-green-300'
                  }`}>
                    Confidence: {(result.confidence * 100).toFixed(1)}%
                  </p>
                </div>
              </div>
              
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.3, type: 'spring', stiffness: 200 }}
                className={`text-4xl font-bold ${
                  result.prediction === 'spam' ? 'text-red-500' : 'text-green-500'
                }`}
              >
                {(result.confidence * 100).toFixed(0)}%
              </motion.div>
            </div>
          </div>

          <div className="p-8 space-y-6">
            {/* Message Display */}
            <div>
              <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Analyzed Message:</h4>
              <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg border border-gray-200 dark:border-gray-600">
                <p className="text-gray-900 dark:text-white whitespace-pre-wrap">{result.message}</p>
              </div>
            </div>

            {/* Prediction Details */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Classification</p>
                <p className={`text-lg font-semibold ${
                  result.prediction === 'spam' ? 'text-red-500' : 'text-green-500'
                }`}>
                  {result.prediction.toUpperCase()}
                </p>
              </div>
              
              <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Confidence Level</p>
                <p className="text-lg font-semibold text-gray-900 dark:text-white">
                  {(result.confidence * 100).toFixed(1)}%
                </p>
              </div>
              
              <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Analysis Time</p>
                <p className="text-lg font-semibold text-gray-900 dark:text-white">
                  {new Date(result.timestamp).toLocaleTimeString()}
                </p>
              </div>
            </div>

            {/* Recommendations */}
            <div className={`p-4 rounded-lg border-l-4 ${
              result.prediction === 'spam' 
                ? 'bg-red-50 dark:bg-red-900/20 border-red-400' 
                : 'bg-green-50 dark:bg-green-900/20 border-green-400'
            }`}>
              <h4 className={`font-medium mb-2 ${
                result.prediction === 'spam' ? 'text-red-800 dark:text-red-300' : 'text-green-800 dark:text-green-300'
              }`}>
                Recommendation
              </h4>
              <p className={`text-sm ${
                result.prediction === 'spam' ? 'text-red-700 dark:text-red-300' : 'text-green-700 dark:text-green-300'
              }`}>
                {result.prediction === 'spam' 
                  ? 'This message appears to be spam. Be cautious about clicking links or responding to requests for personal information.'
                  : 'This message appears to be legitimate. However, always exercise caution with unsolicited messages.'
                }
              </p>
            </div>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 pt-4">
              <Link
                to="/dashboard"
                className="flex-1 flex items-center justify-center px-6 py-3 bg-primary-500 text-white rounded-lg font-medium hover:bg-primary-600 transition-colors"
              >
                <BarChart3 className="h-5 w-5 mr-2" />
                Go to Dashboard
              </Link>
              <Link
                to="/history"
                className="flex-1 flex items-center justify-center px-6 py-3 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 rounded-lg font-medium hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors"
              >
                <History className="h-5 w-5 mr-2" />
                View History
              </Link>
            </div>
          </div>
        </motion.div>
      )}

      {/* Tips for Better Detection */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 p-8"
      >
        <div className="flex items-center mb-6">
          <Lightbulb className="h-6 w-6 text-accent-500 mr-3" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Tips for Better Detection</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-3">
            <h4 className="font-medium text-gray-900 dark:text-white">What makes a message suspicious:</h4>
            <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
              <li>• Urgent language and pressure tactics</li>
              <li>• Requests for personal information</li>
              <li>• Suspicious links and shortened URLs</li>
              <li>• Poor grammar and spelling errors</li>
            </ul>
          </div>
          <div className="space-y-3">
            <h4 className="font-medium text-gray-900 dark:text-white">Signs of legitimate messages:</h4>
            <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
              <li>• Messages from known contacts</li>
              <li>• Professional language and tone</li>
              <li>• Clear sender identification</li>
              <li>• Relevant and contextual content</li>
            </ul>
          </div>
        </div>
      </motion.div>

      {/* Sample Messages */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 p-8"
      >
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Try Sample Messages</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <button
            onClick={() => setMessage('Congratulations! You\'ve won $1000! Click here to claim your prize: bit.ly/claim-now')}
            disabled={loading}
            className="text-left p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg hover:bg-red-100 dark:hover:bg-red-900/30 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <p className="text-sm text-red-700 dark:text-red-300 font-medium mb-1">Spam Example</p>
            <p className="text-xs text-red-600 dark:text-red-400">
              "Congratulations! You've won $1000! Click here to claim..."
            </p>
          </button>
          
          <button
            onClick={() => setMessage('Hi! Are we still meeting for lunch tomorrow at 1pm? Let me know if you need to reschedule.')}
            disabled={loading}
            className="text-left p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg hover:bg-green-100 dark:hover:bg-green-900/30 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <p className="text-sm text-green-700 dark:text-green-300 font-medium mb-1">Ham Example</p>
            <p className="text-xs text-green-600 dark:text-green-400">
              "Hi! Are we still meeting for lunch tomorrow at 1pm?..."
            </p>
          </button>
        </div>
      </motion.div>
    </div>
  );
};

export default Predict;