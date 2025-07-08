import { motion } from 'framer-motion';
import { AlertTriangle, CheckCircle, MessageSquare, Shield, User, Zap } from 'lucide-react';
import React, { useEffect, useState } from 'react';
import { CartesianGrid, Cell, Line, LineChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import LoadingSpinner from '../components/ui/LoadingSpinner';
import { useAuth } from '../contexts/AuthContext';
import { userService } from '../services/api';
import { UserStats } from '../types/index';

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState<UserStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await userService.getUserStats();
        if (response.success && response.data) {
          setStats(response.data);
        } else {
          setError(response.error || 'Failed to fetch statistics');
        }
      } catch (err) {
        setError('Failed to fetch statistics');
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  const pieData = stats ? [
    { name: 'Ham (Safe)', value: stats.hamCount, color: '#10B981' },
    { name: 'Spam', value: stats.spamCount, color: '#EF4444' }
  ] : [];

  const barData = stats ? [
    { name: 'Ham', count: stats.hamCount, color: '#10B981' },
    { name: 'Spam', count: stats.spamCount, color: '#EF4444' }
  ] : [];

  // Generate confidence trend data from recent predictions
  const confidenceTrendData = stats ? stats.recentPredictions
    .slice(0, 10)
    .reverse()
    .map((prediction, index) => ({
      index: index + 1,
      confidence: prediction.confidence * 100,
      type: prediction.prediction
    })) : [];

  // Get the primary accuracy to display
  const getPrimaryAccuracy = () => {
    if (!stats) return 0;

    // If we have the new accuracyData format
    if (stats.accuracyData) {
      const { trainingAccuracy, validationAccuracy, realTimeAccuracy } = stats.accuracyData;

      // Prefer real-time accuracy if available and has enough samples
      if (realTimeAccuracy && stats.totalMessages >= 10) {
        return realTimeAccuracy;
      }
      // Otherwise use validation accuracy
      if (validationAccuracy) {
        return validationAccuracy;
      }
      // Fallback to training accuracy
      return trainingAccuracy;
    }

    // Fallback to old accuracy format
    return stats.accuracy || 0.95;
  };

  const primaryAccuracy = getPrimaryAccuracy();
  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6">
        <p className="text-red-700 dark:text-red-300">{error}</p>
      </div>
    );
  }

  if (!stats || stats.totalMessages === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center py-12"
      >
        <Shield className="h-24 w-24 text-gray-300 dark:text-gray-600 mx-auto mb-6" />
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Welcome to SMS Guard!</h2>
        <p className="text-gray-600 dark:text-gray-400 mb-8">
          You haven't analyzed any messages yet. Start by checking your first message for spam.
        </p>
        <motion.a
          href="/predict"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="inline-flex items-center px-6 py-3 bg-primary-500 text-white rounded-lg font-medium hover:bg-primary-600 transition-colors"
        >
          <MessageSquare className="h-5 w-5 mr-2" />
          Analyze Your First Message
        </motion.a>
      </motion.div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          <User className="inline h-8 w-8 mr-3 text-primary-500" />
          Welcome back, {user?.username}!
        </h1>
        <p className="text-gray-600 dark:text-gray-400">Here's your spam detection activity overview</p>
      </motion.div>

      {/* Main Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Messages</p>
              <p className="text-3xl font-bold text-gray-900 dark:text-white">{stats.totalMessages}</p>
            </div>
            <div className="p-3 bg-primary-100 dark:bg-primary-900/30 rounded-lg">
              <MessageSquare className="h-6 w-6 text-primary-500" />
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Spam Detected</p>
              <p className="text-3xl font-bold text-red-500">{stats.spamCount}</p>
            </div>
            <div className="p-3 bg-red-100 dark:bg-red-900/30 rounded-lg">
              <AlertTriangle className="h-6 w-6 text-red-500" />
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Safe Messages</p>
              <p className="text-3xl font-bold text-green-500">{stats.hamCount}</p>
            </div>
            <div className="p-3 bg-green-100 dark:bg-green-900/30 rounded-lg">
              <CheckCircle className="h-6 w-6 text-green-500" />
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Model Accuracy</p>
              <p className="text-3xl font-bold text-accent-500">{(primaryAccuracy * 100).toFixed(1)}%</p>
            </div>
            <div className="p-3 bg-accent-100 dark:bg-accent-900/30 rounded-lg">
              <Zap className="h-6 w-6 text-accent-500" />
            </div>
          </div>
        </motion.div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Pie Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700"
        >
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Message Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                paddingAngle={5}
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => [`${value} messages`, '']} />
            </PieChart>
          </ResponsiveContainer>
          <div className="flex justify-center space-x-6 mt-4">
            <div className="flex items-center">
              <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
              <span className="text-sm text-gray-600 dark:text-gray-400">Ham (Safe)</span>
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 bg-red-500 rounded-full mr-2"></div>
              <span className="text-sm text-gray-600 dark:text-gray-400">Spam</span>
            </div>
          </div>
        </motion.div>

        {/* Bar Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700"
        >
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Confidence Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={confidenceTrendData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
              <XAxis 
                dataKey="index" 
                stroke="#6B7280" 
                label={{ value: 'Recent Predictions', position: 'insideBottom', offset: -5 }}
              />
              <YAxis stroke="#6B7280" />
              <Tooltip
                formatter={(value) => [`${Number(value).toFixed(1)}%`, 'Confidence']}
                labelFormatter={(label) => `Prediction #${label}`}
                contentStyle={{ 
                  backgroundColor: '#1F2937', 
                  border: 'none', 
                  borderRadius: '8px',
                  color: '#F9FAFB'
                }}
              />
              <Line 
                type="monotone" 
                dataKey="confidence" 
                stroke="#3B82F6" 
                strokeWidth={3}
                dot={{ fill: '#3B82F6', strokeWidth: 2, r: 4 }}
                activeDot={{ r: 6, stroke: '#3B82F6', strokeWidth: 2 }}
              />
            </LineChart>
          </ResponsiveContainer>
          {confidenceTrendData.length === 0 && (
            <div className="flex items-center justify-center h-64 text-gray-500 dark:text-gray-400">
              <p>No prediction data available yet</p>
            </div>
          )}
        </motion.div>
      </div>

      {/* Recent Activity */}
      {stats.recentPredictions.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700"
        >
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Recent Predictions</h3>
          </div>
          <div className="p-6">
            <div className="space-y-4">
              {stats.recentPredictions.slice(0, 5).map((prediction, index) => (
                <motion.div
                  key={prediction.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.8 + index * 0.1 }}
                  className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg"
                >
                  <div className="flex-1 min-w-0 mr-4">
                    <p className="text-sm text-gray-900 dark:text-white truncate">{prediction.message}</p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      {new Date(prediction.timestamp).toLocaleString()}
                    </p>
                  </div>
                  <div className="flex items-center space-x-3">
                    {/* Horizontal confidence bar */}
                    <div className="w-20 h-2 bg-gray-200 dark:bg-gray-600 rounded-full overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${prediction.confidence * 100}%` }}
                        transition={{ delay: 0.9 + index * 0.1, duration: 0.8 }}
                        className={`h-full ${
                          prediction.prediction === 'spam' ? 'bg-red-500' : 'bg-green-500'
                        }`}
                      />
                    </div>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                      prediction.prediction === 'spam' 
                        ? 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300' 
                        : 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300'
                    }`}>
                      {prediction.prediction.toUpperCase()}
                    </span>
                    <span className="text-xs text-gray-500 dark:text-gray-400 min-w-[3rem] text-right">
                      {(prediction.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </motion.div>
      )}

      {/* Personal Insights Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
        className="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700 p-6"
      >
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">Personal Insights</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <div className="text-3xl font-bold text-red-500 mb-2">
              {(stats.spamRate * 100).toFixed(1)}%
            </div>
            <div className="text-sm font-medium text-gray-900 dark:text-white mb-1">Spam Rate</div>
            <div className="text-xs text-gray-500 dark:text-gray-400">Of your analyzed messages</div>
          </div>
          
          <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <div className="text-3xl font-bold text-blue-500 mb-2">
              {(stats.avgConfidence * 100).toFixed(1)}%
            </div>
            <div className="text-sm font-medium text-gray-900 dark:text-white mb-1">Avg Confidence</div>
            <div className="text-xs text-gray-500 dark:text-gray-400">Recent predictions</div>
          </div>
          
          <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <div className="text-3xl font-bold text-green-500 mb-2">
              {stats.totalMessages}
            </div>
            <div className="text-sm font-medium text-gray-900 dark:text-white mb-1">Total Analyzed</div>
            <div className="text-xs text-gray-500 dark:text-gray-400">Messages processed</div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Dashboard;