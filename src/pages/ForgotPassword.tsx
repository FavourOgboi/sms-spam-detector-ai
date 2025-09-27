import { motion } from 'framer-motion';
import { ArrowLeft, Mail, Send } from 'lucide-react';
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import LoadingSpinner from '../components/ui/LoadingSpinner';
import { authService } from '../services/api';

const ForgotPassword: React.FC = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [resetLinkSent, setResetLinkSent] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setMessage('');

    try {
      console.log('🔄 Sending forgot password request for:', email);

      const result = await authService.forgotPassword(email);

      if (result.success && result.data) {
        setMessage(result.data.message || 'Password reset link sent to your email.');
        setResetLinkSent(true);
        
        // Show reset link in development mode
        if (result.data.resetLink && result.data.debug) {
          console.log('🔗 Reset link (development):', result.data.resetLink);
          setMessage(result.data.message + ' (Check console for reset link in development mode)');
        }
      } else {
        setError(result.error || 'Failed to send reset link.');
      }
    } catch (err) {
      console.error('❌ Network error:', err);
      setError('Network error. Make sure the backend is running on http://localhost:5000');
    }
    
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8"
        >
          {/* Header */}
          <div className="text-center mb-8">
            <div className="mx-auto w-16 h-16 bg-primary-100 dark:bg-primary-900 rounded-full flex items-center justify-center mb-4">
              <Mail className="w-8 h-8 text-primary-600 dark:text-primary-400" />
            </div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              Forgot Password?
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              Enter your email address and we'll send you a link to reset your password.
            </p>
          </div>

          {!resetLinkSent ? (
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Email Address
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                  <input
                    type="email"
                    id="email"
                    name="email"
                    autoComplete="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200"
                    placeholder="Enter your email address"
                    required
                    disabled={loading}
                  />
                </div>
              </div>

              {error && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4"
                >
                  <p className="text-red-600 dark:text-red-400 text-sm">{error}</p>
                </motion.div>
              )}

              <motion.button
                type="submit"
                disabled={loading || !email.trim()}
                whileHover={{ scale: loading ? 1 : 1.02 }}
                whileTap={{ scale: loading ? 1 : 0.98 }}
                className="w-full bg-primary-500 text-white py-3 px-4 rounded-lg font-medium hover:bg-primary-600 focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center justify-center"
              >
                {loading ? (
                  <LoadingSpinner size="sm" />
                ) : (
                  <>
                    <Send className="w-5 h-5 mr-2" />
                    Send Reset Link
                  </>
                )}
              </motion.button>
            </form>
          ) : (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="text-center space-y-4"
            >
              <div className="mx-auto w-16 h-16 bg-green-100 dark:bg-green-900 rounded-full flex items-center justify-center mb-4">
                <Send className="w-8 h-8 text-green-600 dark:text-green-400" />
              </div>
              <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
                <p className="text-green-600 dark:text-green-400 text-sm">{message}</p>
              </div>
              <p className="text-gray-600 dark:text-gray-400 text-sm">
                Check your email inbox and click the reset link to continue.
              </p>
            </motion.div>
          )}

          {/* Back to Login */}
          <div className="mt-8 text-center">
            <Link
              to="/login"
              className="inline-flex items-center text-primary-500 hover:text-primary-600 font-medium transition-colors duration-200"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Login
            </Link>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default ForgotPassword;
