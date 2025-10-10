import { motion } from 'framer-motion';
import { CheckCircle, Eye, EyeOff, Lock, Shield } from 'lucide-react';
import React, { useEffect, useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import LoadingSpinner from '../components/ui/LoadingSpinner';
import { useAuthService } from '../services/api';

const ResetPassword: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const token = searchParams.get('token');
  const userId = searchParams.get('user_id');

  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const { resetPassword } = useAuthService();

  useEffect(() => {
    console.log('🔍 URL Parameters:', { token, userId });
    console.log('🔍 Token length:', token?.length);
    console.log('🔍 User ID length:', userId?.length);

    if (!token) {
      console.log('❌ No token found in URL');
      setError('Invalid reset link. Please request a new password reset.');
      return;
    }

    // User ID is optional for some implementations
    if (!userId) {
      console.log('⚠️ No user ID found in URL (may be optional)');
    }
  }, [token, userId]);

  const validatePassword = (password: string) => {
    if (password.length < 8) {
      return 'Password must be at least 8 characters long';
    }
    if (!/(?=.*[a-z])/.test(password)) {
      return 'Password must contain at least one lowercase letter';
    }
    if (!/(?=.*[A-Z])/.test(password)) {
      return 'Password must contain at least one uppercase letter';
    }
    if (!/(?=.*\d)/.test(password)) {
      return 'Password must contain at least one number';
    }
    if (!/(?=.*[@$!%*?&])/.test(password)) {
      return 'Password must contain at least one special character (@$!%*?&)';
    }
    return null;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!token) {
      setError('Invalid reset token');
      return;
    }

    // User ID is optional - don't block if missing
    console.log('🔄 Proceeding with reset:', { hasToken: !!token, hasUserId: !!userId });

    if (!password || !confirmPassword) {
      setError('Please fill in all fields');
      return;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    const passwordError = validatePassword(password);
    if (passwordError) {
      setError(passwordError);
      return;
    }

    setLoading(true);
    setError('');

    try {
      console.log('🔄 Resetting password with token:', token.substring(0, 10) + '...');
      console.log('🔄 Using user ID:', userId);

      const result = await resetPassword(token, password, userId || undefined);

      if (result.success) {
        setSuccess(true);
        console.log('✅ Password reset successful');
        
        // Redirect to login after 3 seconds
        setTimeout(() => {
          navigate('/login', {
            state: {
              message: 'Password reset successful! Please log in with your new password.',
              type: 'success'
            }
          });
        }, 3000);
      } else {
        setError(result.error || 'Failed to reset password');
      }
    } catch (err) {
      console.error('❌ Reset password error:', err);
      setError('Network error. Please try again.');
    }

    setLoading(false);
  };

  if (!token) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4">
        <div className="w-full max-w-md">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 text-center"
          >
            <div className="mx-auto w-16 h-16 bg-red-100 dark:bg-red-900 rounded-full flex items-center justify-center mb-4">
              <Shield className="w-8 h-8 text-red-600 dark:text-red-400" />
            </div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
              Invalid Reset Link
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              This password reset link is invalid or has expired. Please request a new one.
            </p>
            <Link
              to="/forgot-password"
              className="inline-block bg-primary-500 text-white py-2 px-6 rounded-lg font-medium hover:bg-primary-600 transition-colors duration-200"
            >
              Request New Reset Link
            </Link>
          </motion.div>
        </div>
      </div>
    );
  }

  if (success) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4">
        <div className="w-full max-w-md">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 text-center"
          >
            <div className="mx-auto w-16 h-16 bg-green-100 dark:bg-green-900 rounded-full flex items-center justify-center mb-4">
              <CheckCircle className="w-8 h-8 text-green-600 dark:text-green-400" />
            </div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
              Password Reset Successful!
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              Your password has been successfully reset. You will be redirected to the login page shortly.
            </p>
            <div className="flex items-center justify-center">
              <LoadingSpinner size="sm" />
              <span className="ml-2 text-sm text-gray-500">Redirecting...</span>
            </div>
          </motion.div>
        </div>
      </div>
    );
  }

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
              <Lock className="w-8 h-8 text-primary-600 dark:text-primary-400" />
            </div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              Reset Your Password
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              Enter your new password below
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* New Password */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                New Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full pl-10 pr-12 py-3 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200"
                  placeholder="Enter new password"
                  required
                  disabled={loading}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                  disabled={loading}
                >
                  {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                </button>
              </div>
            </div>

            {/* Confirm Password */}
            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Confirm New Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  type={showConfirmPassword ? 'text' : 'password'}
                  id="confirmPassword"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="w-full pl-10 pr-12 py-3 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200"
                  placeholder="Confirm new password"
                  required
                  disabled={loading}
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                  disabled={loading}
                >
                  {showConfirmPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                </button>
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
              disabled={loading || !password || !confirmPassword}
              whileHover={{ scale: loading ? 1 : 1.02 }}
              whileTap={{ scale: loading ? 1 : 0.98 }}
              className="w-full bg-primary-500 text-white py-3 px-4 rounded-lg font-medium hover:bg-primary-600 focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
            >
              {loading ? <LoadingSpinner size="sm" /> : 'Reset Password'}
            </motion.button>
          </form>

          {/* Back to Login */}
          <div className="mt-8 text-center">
            <Link
              to="/login"
              className="text-primary-500 hover:text-primary-600 font-medium transition-colors duration-200"
            >
              Back to Login
            </Link>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default ResetPassword;
