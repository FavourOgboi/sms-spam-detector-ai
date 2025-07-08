import { motion } from 'framer-motion';
import { BarChart3, History, Lightbulb, Send } from 'lucide-react';
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import GuardAnimation from '../components/ui/GuardAnimation';
import LoadingSpinner from '../components/ui/LoadingSpinner';
import { predictionService } from '../services/api';
import { PredictionResult } from '../types/index';

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

      {/* Results with Explainable AI */}
      {result && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <ExplainableAI
            prediction={result.prediction}
            confidence={result.confidence}
            spamProbability={result.spamProbability}
            hamProbability={result.hamProbability}
            explanations={result.topFeatures || []}
            message={result.message}
          />

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 mt-6">
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
            <button
              type="button"
              onClick={resetForm}
              className="flex-1 flex items-center justify-center px-6 py-3 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 rounded-lg font-medium hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors"
            >
              Analyze Another Message
            </button>
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
            type="button"
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
            type="button"
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