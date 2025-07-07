import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Search, Filter, MessageSquare, AlertTriangle, CheckCircle, Calendar, Download } from 'lucide-react';
import { userService } from '../services/api';
import { PredictionResult } from '../types/index';
import LoadingSpinner from '../components/ui/LoadingSpinner';

const History: React.FC = () => {
  const [predictions, setPredictions] = useState<PredictionResult[]>([]);
  const [filteredPredictions, setFilteredPredictions] = useState<PredictionResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState<'all' | 'spam' | 'ham'>('all');
  const [downloadLoading, setDownloadLoading] = useState(false);

  useEffect(() => {
    const fetchPredictions = async () => {
      try {
        const response = await userService.getUserPredictions();
        if (response.success && response.data) {
          setPredictions(response.data);
          setFilteredPredictions(response.data);
        } else {
          setError(response.error || 'Failed to fetch predictions');
        }
      } catch (err) {
        setError('Failed to fetch predictions');
      } finally {
        setLoading(false);
      }
    };

    fetchPredictions();
  }, []);

  useEffect(() => {
    let filtered = predictions;

    // Apply filter
    if (filter !== 'all') {
      filtered = filtered.filter(p => p.prediction === filter);
    }

    // Apply search
    if (searchTerm) {
      filtered = filtered.filter(p => 
        p.message.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    setFilteredPredictions(filtered);
  }, [predictions, filter, searchTerm]);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return {
      date: date.toLocaleDateString(),
      time: date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
  };

  const downloadCSV = () => {
    setDownloadLoading(true);
    
    try {
      // Prepare CSV data
      const csvHeaders = ['Message', 'Prediction', 'Confidence', 'Timestamp'];
      const csvData = filteredPredictions.map(prediction => [
        `"${prediction.message.replace(/"/g, '""')}"`, // Escape quotes in message
        prediction.prediction,
        (prediction.confidence * 100).toFixed(1) + '%',
        new Date(prediction.timestamp).toLocaleString()
      ]);
      
      // Create CSV content
      const csvContent = [
        csvHeaders.join(','),
        ...csvData.map(row => row.join(','))
      ].join('\n');
      
      // Create and download file
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      const url = URL.createObjectURL(blob);
      link.setAttribute('href', url);
      link.setAttribute('download', `spam-predictions-${new Date().toISOString().split('T')[0]}.csv`);
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Failed to download CSV:', error);
    } finally {
      setDownloadLoading(false);
    }
  };
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

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex flex-col sm:flex-row sm:items-center sm:justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Message History</h1>
          <p className="text-gray-600 dark:text-gray-400">
            View and search through your past spam detection results
          </p>
        </div>
        <div className="mt-4 sm:mt-0 flex items-center space-x-4">
          <div className="text-sm text-gray-500 dark:text-gray-400">
            {filteredPredictions.length} of {predictions.length} messages
          </div>
          {filteredPredictions.length > 0 && (
            <motion.button
              onClick={downloadCSV}
              disabled={downloadLoading}
              whileHover={{ scale: downloadLoading ? 1 : 1.05 }}
              whileTap={{ scale: downloadLoading ? 1 : 0.95 }}
              className="flex items-center px-4 py-2 bg-primary-500 text-white rounded-lg font-medium hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
            >
              {downloadLoading ? (
                <LoadingSpinner size="sm" className="mr-2" />
              ) : (
                <Download className="h-4 w-4 mr-2" />
              )}
              {downloadLoading ? 'Preparing...' : 'Download CSV'}
            </motion.button>
          )}
        </div>
      </motion.div>

      {/* Search and Filter */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700 p-6"
      >
        <div className="flex flex-col sm:flex-row gap-4">
          {/* Search */}
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search messages..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>

          {/* Filter */}
          <div className="relative">
            <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <select
              value={filter}
              onChange={(e) => setFilter(e.target.value as 'all' | 'spam' | 'ham')}
              className="pl-10 pr-8 py-3 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent appearance-none min-w-32"
            >
              <option value="all">All Messages</option>
              <option value="spam">Spam Only</option>
              <option value="ham">Ham Only</option>
            </select>
          </div>
        </div>
      </motion.div>

      {/* Results */}
      {filteredPredictions.length === 0 ? (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="text-center py-12"
        >
          <MessageSquare className="h-24 w-24 text-gray-300 dark:text-gray-600 mx-auto mb-6" />
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
            {searchTerm || filter !== 'all' ? 'No matching messages found' : 'No messages yet'}
          </h3>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            {searchTerm || filter !== 'all' 
              ? 'Try adjusting your search or filter criteria.'
              : 'Start by analyzing your first message for spam detection.'
            }
          </p>
          {(!searchTerm && filter === 'all') && (
            <motion.a
              href="/predict"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="inline-flex items-center px-6 py-3 bg-primary-500 text-white rounded-lg font-medium hover:bg-primary-600 transition-colors"
            >
              <MessageSquare className="h-5 w-5 mr-2" />
              Analyze Your First Message
            </motion.a>
          )}
        </motion.div>
      ) : (
        <div className="space-y-4">
          {filteredPredictions.map((prediction, index) => {
            const { date, time } = formatDate(prediction.timestamp);
            
            return (
              <motion.div
                key={prediction.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 + index * 0.05 }}
                className="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700 p-6 hover:shadow-xl transition-shadow duration-200"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center space-x-3">
                    {prediction.prediction === 'spam' ? (
                      <div className="p-2 bg-red-100 dark:bg-red-900/30 rounded-lg">
                        <AlertTriangle className="h-5 w-5 text-red-500" />
                      </div>
                    ) : (
                      <div className="p-2 bg-green-100 dark:bg-green-900/30 rounded-lg">
                        <CheckCircle className="h-5 w-5 text-green-500" />
                      </div>
                    )}
                    <div>
                      <span className={`px-3 py-1 text-sm font-medium rounded-full ${
                        prediction.prediction === 'spam'
                          ? 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300'
                          : 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300'
                      }`}>
                        {prediction.prediction.toUpperCase()}
                      </span>
                      <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                        Confidence: {(prediction.confidence * 100).toFixed(1)}%
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-2 text-sm text-gray-500 dark:text-gray-400">
                    <Calendar className="h-4 w-4" />
                    <span>{date}</span>
                    <span>{time}</span>
                  </div>
                </div>

                <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 border border-gray-200 dark:border-gray-600">
                  <p className="text-gray-900 dark:text-white whitespace-pre-wrap break-words">
                    {prediction.message}
                  </p>
                </div>

                {/* Confidence Bar */}
                <div className="mt-4">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Confidence Level</span>
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                      {(prediction.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${prediction.confidence * 100}%` }}
                      transition={{ delay: 0.3 + index * 0.05, duration: 0.8 }}
                      className={`h-2 rounded-full ${
                        prediction.prediction === 'spam' ? 'bg-red-500' : 'bg-green-500'
                      }`}
                    />
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default History;