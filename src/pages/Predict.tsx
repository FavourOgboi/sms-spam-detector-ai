import { motion } from 'framer-motion';
import {
    AlertTriangle,
    BarChart3,
    CheckCircle,
    History,
    Lightbulb,
    Send
} from 'lucide-react';
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
  const [explanation, setExplanation] = useState<any>(null);
  const [loadingExplanation, setLoadingExplanation] = useState(false);
  const [error, setError] = useState('');

  const resetForm = () => {
    setMessage('');
    setResult(null);
    setExplanation(null);
    setError('');
  };

  const handleExplain = async () => {
    if (!message.trim()) {
      setError('SMS message cannot be empty');
      return;
    }

    setLoadingExplanation(true);
    setError('');

    try {
      console.log('🔍 Requesting explanation for message:', message.substring(0, 50) + '...');
      const response = await predictionService.explainPrediction(message, 10);

      if (response.success && response.data) {
        console.log('✅ Explanation received:', response.data);
        setExplanation(response.data);
      } else {
        console.log('❌ Explanation failed:', response.error);
        setError(response.error || 'Explanation failed');
      }
    } catch (err) {
      console.error('❌ Explanation error:', err);
      setError('Explanation failed. Please try again.');
    } finally {
      setLoadingExplanation(false);
    }
  };

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

            {/* Basic AI Explanation */}
            {result.explanation && result.explanation.top_features && result.explanation.top_features.length > 0 && (
              <div className="bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 p-6 rounded-lg border border-purple-200 dark:border-purple-800">
                <div className="flex items-center mb-4">
                  <div className="p-2 bg-purple-100 dark:bg-purple-900/50 rounded-lg mr-3">
                    <Lightbulb className="h-5 w-5 text-purple-600 dark:text-purple-400" />
                  </div>
                  <h4 className="text-lg font-semibold text-purple-900 dark:text-purple-100">
                    AI Explanation ({result.explanation.method})
                  </h4>
                </div>

                <p className="text-sm text-purple-700 dark:text-purple-300 mb-4">
                  {result.explanation.summary}
                </p>

                <div className="space-y-2">
                  <h5 className="text-sm font-medium text-purple-800 dark:text-purple-200 mb-2">
                    Key Contributing Words:
                  </h5>
                  <div className="flex flex-wrap gap-2">
                    {result.explanation.top_features.map((feature, index) => (
                      <motion.span
                        key={index}
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: index * 0.1 }}
                        className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${
                          feature.direction === 'spam'
                            ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300'
                            : 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300'
                        }`}
                      >
                        "{feature.feature}"
                        <span className="ml-1 text-xs opacity-75">
                          {feature.direction === 'spam' ? '→ SPAM' : '→ HAM'}
                        </span>
                        <span className="ml-1 text-xs opacity-60">
                          ({Math.abs(feature.importance).toFixed(2)})
                        </span>
                      </motion.span>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Why this prediction? */}
            {result.topFeatures && result.topFeatures.length > 0 && (
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 p-6 rounded-lg border border-blue-200 dark:border-blue-800">
                <div className="flex items-center mb-4">
                  <div className="p-2 bg-blue-100 dark:bg-blue-900/50 rounded-lg mr-3">
                    <svg className="h-5 w-5 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                  <h4 className="text-lg font-semibold text-blue-900 dark:text-blue-100">
                    Why this prediction?
                  </h4>
                </div>

                <p className="text-sm text-blue-700 dark:text-blue-300 mb-4">
                  Our AI analyzed these key patterns in your message:
                </p>

                <div className="space-y-3">
                  {result.topFeatures.map((feature, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className="flex items-start space-x-3 p-3 bg-white dark:bg-gray-800 rounded-lg border border-blue-100 dark:border-blue-800"
                    >
                      <div className="flex-shrink-0">
                        {feature.method === 'KEYWORD' && (
                          <div className="p-1.5 bg-orange-100 dark:bg-orange-900/50 rounded-full">
                            <svg className="h-4 w-4 text-orange-600 dark:text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                            </svg>
                          </div>
                        )}
                        {feature.method === 'ANALYSIS' && (
                          <div className="p-1.5 bg-purple-100 dark:bg-purple-900/50 rounded-full">
                            <svg className="h-4 w-4 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                            </svg>
                          </div>
                        )}
                      </div>

                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between mb-1">
                          <h5 className="text-sm font-medium text-gray-900 dark:text-white capitalize">
                            {feature.feature.replace(/_/g, ' ')}
                          </h5>
                          <div className="flex items-center space-x-2">
                            <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                              feature.method === 'KEYWORD'
                                ? 'bg-orange-100 text-orange-800 dark:bg-orange-900/50 dark:text-orange-300'
                                : 'bg-purple-100 text-purple-800 dark:bg-purple-900/50 dark:text-purple-300'
                            }`}>
                              {feature.method}
                            </span>
                            <div className="flex items-center">
                              <div className={`h-2 w-16 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden`}>
                                <div
                                  className={`h-full transition-all duration-500 ${
                                    feature.importance > 0.7 ? 'bg-red-500' :
                                    feature.importance > 0.4 ? 'bg-yellow-500' : 'bg-green-500'
                                  }`}
                                  style={{ width: `${Math.min(feature.importance * 100, 100)}%` }}
                                />
                              </div>
                              <span className="ml-2 text-xs text-gray-500 dark:text-gray-400">
                                {(feature.importance * 100).toFixed(0)}%
                              </span>
                            </div>
                          </div>
                        </div>
                        <p className="text-sm text-gray-600 dark:text-gray-300">
                          {feature.explanation}
                        </p>
                      </div>
                    </motion.div>
                  ))}
                </div>

                <div className="mt-4 p-3 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
                  <p className="text-xs text-blue-700 dark:text-blue-300">
                    <strong>How it works:</strong> Our AI examines multiple factors including keywords, message structure,
                    capitalization patterns, and punctuation to determine if a message is spam or legitimate.
                  </p>
                </div>
              </div>
            )}

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
              <button
                type="button"
                onClick={handleExplain}
                disabled={loadingExplanation}
                className="flex-1 flex items-center justify-center px-6 py-3 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {loadingExplanation ? (
                  <LoadingSpinner size="sm" className="mr-2" />
                ) : (
                  <Lightbulb className="h-5 w-5 mr-2" />
                )}
                {loadingExplanation ? 'Explaining...' : 'Explain Prediction'}
              </button>
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
          </div>
        </motion.div>
      )}

      {/* Explanation Results */}
      {explanation && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 overflow-hidden"
        >
          <div className="bg-gradient-to-r from-blue-500 to-indigo-500 p-6 text-white">
            <div className="flex items-center space-x-3">
              <Lightbulb className="h-8 w-8" />
              <div>
                <h3 className="text-2xl font-bold">AI Explanation</h3>
                <p className="text-blue-100">Understanding why this prediction was made</p>
              </div>
            </div>
          </div>

          <div className="p-8 space-y-6">
            {explanation.success ? (
              <>
                {/* Prediction Summary */}
                <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                  <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Prediction Summary</h4>
                  <p className="text-gray-700 dark:text-gray-300">
                    <strong>Result:</strong> {explanation.prediction?.toUpperCase()}
                    <span className="ml-2">
                      (Confidence: {explanation.confidence ? (explanation.confidence * 100).toFixed(1) : 'N/A'}%)
                    </span>
                  </p>
                  {explanation.explanation?.summary && (
                    <p className="text-gray-600 dark:text-gray-400 mt-2">
                      {explanation.explanation.summary}
                    </p>
                  )}
                </div>

                {/* Feature Analysis */}
                {explanation.explanation?.features && explanation.explanation.features.length > 0 && (
                  <div>
                    <h4 className="font-semibold text-gray-900 dark:text-white mb-4">
                      Key Features Analysis ({explanation.explanation.method})
                    </h4>
                    <div className="space-y-3">
                      {explanation.explanation.features.slice(0, 8).map((feature: any, index: number) => (
                        <motion.div
                          key={index}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: index * 0.1 }}
                          className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg border-l-4 border-l-blue-500"
                        >
                          <div className="flex items-center justify-between mb-3">
                            <div className="flex items-center space-x-3">
                              <div className={`w-4 h-4 rounded-full flex items-center justify-center ${
                                feature.direction === 'spam' ? 'bg-red-500' : 'bg-green-500'
                              }`}>
                                <span className="text-white text-xs font-bold">
                                  {feature.direction === 'spam' ? '!' : '✓'}
                                </span>
                              </div>
                              <div>
                                <span className="font-semibold text-gray-900 dark:text-white text-lg">
                                  "{feature.feature}"
                                </span>
                                <span className={`ml-3 text-xs px-2 py-1 rounded-full font-medium ${
                                  feature.direction === 'spam'
                                    ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300'
                                    : 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300'
                                }`}>
                                  {feature.direction === 'spam' ? 'SPAM SIGNAL' : 'LEGITIMATE SIGNAL'}
                                </span>
                              </div>
                            </div>
                          </div>

                          <div className="grid grid-cols-2 gap-3 mt-3">
                            <div className="text-center p-2 bg-white dark:bg-gray-600 rounded">
                              <div className="text-lg font-bold text-gray-900 dark:text-white">
                                {Math.abs(feature.importance || 0).toFixed(4)}
                              </div>
                              <div className="text-xs text-gray-500 dark:text-gray-400">
                                Model Weight
                              </div>
                            </div>

                            <div className="text-center p-2 bg-white dark:bg-gray-600 rounded">
                              <div className="text-lg font-bold text-gray-900 dark:text-white">
                                {(feature.frequency || feature.tf_idf_score || 0).toFixed(4)}
                              </div>
                              <div className="text-xs text-gray-500 dark:text-gray-400">
                                TF-IDF Score
                              </div>
                            </div>
                          </div>

                          <div className="mt-3 text-sm text-gray-600 dark:text-gray-300">
                            <strong>Your model learned:</strong> This word is a{' '}
                            <span className={feature.direction === 'spam' ? 'text-red-600 dark:text-red-400 font-semibold' : 'text-green-600 dark:text-green-400 font-semibold'}>
                              {feature.direction === 'spam' ? 'spam indicator' : 'legitimate indicator'}
                            </span>{' '}
                            from your training data.
                          </div>
                        </motion.div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Spam vs Ham Indicators Summary */}
                {explanation.explanation?.spam_indicators || explanation.explanation?.ham_indicators ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Spam Indicators */}
                    {explanation.explanation.spam_indicators && explanation.explanation.spam_indicators.length > 0 && (
                      <div className="bg-red-50 dark:bg-red-900/20 p-4 rounded-lg border border-red-200 dark:border-red-800">
                        <h5 className="font-semibold text-red-800 dark:text-red-300 mb-3 flex items-center">
                          <span className="w-3 h-3 bg-red-500 rounded-full mr-2"></span>
                          SPAM Indicators ({explanation.explanation.spam_indicators.length})
                        </h5>
                        <div className="space-y-2">
                          {explanation.explanation.spam_indicators.slice(0, 5).map((indicator: any, idx: number) => (
                            <div key={idx} className="flex items-center justify-between text-sm">
                              <span className="text-red-700 dark:text-red-300 font-medium">
                                "{indicator.feature}"
                              </span>
                              <span className="text-red-600 dark:text-red-400 text-xs">
                                {Math.abs(indicator.importance).toFixed(3)}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Ham Indicators */}
                    {explanation.explanation.ham_indicators && explanation.explanation.ham_indicators.length > 0 && (
                      <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg border border-green-200 dark:border-green-800">
                        <h5 className="font-semibold text-green-800 dark:text-green-300 mb-3 flex items-center">
                          <span className="w-3 h-3 bg-green-500 rounded-full mr-2"></span>
                          LEGITIMATE Indicators ({explanation.explanation.ham_indicators.length})
                        </h5>
                        <div className="space-y-2">
                          {explanation.explanation.ham_indicators.slice(0, 5).map((indicator: any, idx: number) => (
                            <div key={idx} className="flex items-center justify-between text-sm">
                              <span className="text-green-700 dark:text-green-300 font-medium">
                                "{indicator.feature}"
                              </span>
                              <span className="text-green-600 dark:text-green-400 text-xs">
                                {Math.abs(indicator.importance).toFixed(3)}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ) : null}

                {/* Processing Info */}
                <div className="text-sm text-gray-500 dark:text-gray-400 border-t border-gray-200 dark:border-gray-600 pt-4">
                  <p>
                    Analysis completed in {explanation.processing_time_ms || 'N/A'}ms using {explanation.explanation?.method || 'AI'} method
                  </p>
                </div>
              </>
            ) : (
              <div className="text-center py-8">
                <div className="text-yellow-500 mb-4">
                  <Lightbulb className="h-12 w-12 mx-auto" />
                </div>
                <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  Explanation Not Available
                </h4>
                <p className="text-gray-600 dark:text-gray-400 mb-4">
                  {explanation.error || 'Unable to generate explanation for this prediction.'}
                </p>
                {explanation.fallback_explanation && (
                  <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg text-left">
                    <h5 className="font-medium text-gray-900 dark:text-white mb-2">
                      Basic Analysis ({explanation.fallback_explanation.method})
                    </h5>
                    <p className="text-gray-600 dark:text-gray-400 mb-3">
                      {explanation.fallback_explanation.summary}
                    </p>
                    {explanation.fallback_explanation.features && explanation.fallback_explanation.features.length > 0 && (
                      <div className="space-y-2">
                        {explanation.fallback_explanation.features.map((feature: any, index: number) => (
                          <div key={index} className="flex items-center space-x-2">
                            <div className="w-2 h-2 bg-orange-500 rounded-full"></div>
                            <span className="text-sm text-gray-700 dark:text-gray-300">
                              Found keyword: "{feature.feature}"
                            </span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
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