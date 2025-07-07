import React from 'react';
import { motion } from 'framer-motion';
import { Brain, Database, Shield, Zap, CheckCircle, AlertTriangle, ArrowRight, Clock, Cpu, Search, BarChart3 } from 'lucide-react';

const Explanation: React.FC = () => {
  const features = [
    {
      icon: Brain,
      title: 'Advanced AI Algorithm',
      description: 'Our model uses cutting-edge natural language processing and deep learning techniques to analyze message patterns, keywords, and linguistic features that commonly appear in spam messages.',
      color: 'bg-gradient-to-br from-blue-500 to-blue-600',
      iconColor: 'text-white'
    },
    {
      icon: Database,
      title: 'Comprehensive Training Data',
      description: 'Trained on millions of real SMS messages from diverse sources, ensuring high accuracy and low false positive rates across different message types and languages.',
      color: 'bg-gradient-to-br from-green-500 to-green-600',
      iconColor: 'text-white'
    },
    {
      icon: Shield,
      title: 'Real-time Protection',
      description: 'Instant analysis of your messages with confidence scores and detailed explanations, helping you make informed decisions about potentially suspicious communications.',
      color: 'bg-gradient-to-br from-purple-500 to-purple-600',
      iconColor: 'text-white'
    },
    {
      icon: Zap,
      title: 'Lightning Fast Performance',
      description: 'Optimized for speed and accuracy, our model processes messages in milliseconds while maintaining industry-leading detection rates and minimal resource usage.',
      color: 'bg-gradient-to-br from-orange-500 to-orange-600',
      iconColor: 'text-white'
    }
  ];

  const detectionSteps = [
    {
      step: 1,
      title: 'Message Input',
      description: 'User submits SMS message for analysis through our secure interface',
      icon: Search,
      color: 'bg-blue-500',
      details: ['Text normalization', 'Character encoding', 'Input validation']
    },
    {
      step: 2,
      title: 'Text Preprocessing',
      description: 'Message is cleaned, tokenized, and prepared for feature extraction',
      icon: Cpu,
      color: 'bg-indigo-500',
      details: ['Remove special characters', 'Lowercase conversion', 'Tokenization', 'Stop word removal']
    },
    {
      step: 3,
      title: 'Feature Extraction',
      description: 'Key linguistic features and patterns are identified and quantified',
      icon: BarChart3,
      color: 'bg-purple-500',
      details: ['N-gram analysis', 'Keyword detection', 'Sentiment analysis', 'URL pattern matching']
    },
    {
      step: 4,
      title: 'AI Model Analysis',
      description: 'Machine learning model processes features to determine spam probability',
      icon: Brain,
      color: 'bg-pink-500',
      details: ['Neural network processing', 'Pattern recognition', 'Probability calculation', 'Confidence scoring']
    },
    {
      step: 5,
      title: 'Result Generation',
      description: 'Final classification with confidence score and detailed explanation',
      icon: CheckCircle,
      color: 'bg-green-500',
      details: ['Classification decision', 'Confidence percentage', 'Risk assessment', 'Recommendation']
    }
  ];

  const spamIndicators = [
    { text: 'Urgent language and pressure tactics', severity: 'high' },
    { text: 'Requests for personal information', severity: 'high' },
    { text: 'Suspicious links and shortened URLs', severity: 'high' },
    { text: 'Poor grammar and spelling errors', severity: 'medium' },
    { text: 'Excessive use of capital letters', severity: 'medium' },
    { text: 'Promises of free money or prizes', severity: 'high' },
    { text: 'Unknown sender requesting action', severity: 'medium' }
  ];

  const safeIndicators = [
    { text: 'Messages from known contacts', severity: 'safe' },
    { text: 'Professional language and tone', severity: 'safe' },
    { text: 'Legitimate business communications', severity: 'safe' },
    { text: 'Personal conversations', severity: 'safe' },
    { text: 'Clear sender identification', severity: 'safe' },
    { text: 'Relevant and contextual content', severity: 'safe' },
    { text: 'No suspicious links or attachments', severity: 'safe' }
  ];

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high': return 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300 border-red-200 dark:border-red-800';
      case 'medium': return 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300 border-yellow-200 dark:border-yellow-800';
      case 'safe': return 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300 border-green-200 dark:border-green-800';
      default: return 'bg-gray-100 dark:bg-gray-900/30 text-gray-800 dark:text-gray-300 border-gray-200 dark:border-gray-800';
    }
  };

  return (
    <div className="max-w-7xl mx-auto space-y-16">
      {/* Hero Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center relative overflow-hidden"
      >
        <div className="absolute inset-0 bg-gradient-to-r from-primary-500/10 to-accent-500/10 rounded-3xl"></div>
        <div className="relative z-10 py-16 px-8">
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-primary-500 to-accent-500 rounded-full mb-8"
          >
            <Shield className="h-10 w-10 text-white" />
          </motion.div>
          <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-6">
            How <span className="bg-gradient-to-r from-primary-500 to-accent-500 bg-clip-text text-transparent">SMS Guard</span> Works
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto leading-relaxed">
            Discover the advanced technology and machine learning algorithms that power this 
            state-of-the-art SMS spam detection system
          </p>
        </div>
      </motion.div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {features.map((feature, index) => (
          <motion.div
            key={feature.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="group relative bg-white dark:bg-gray-800 rounded-3xl shadow-xl border border-gray-100 dark:border-gray-700 p-8 hover:shadow-2xl transition-all duration-300 overflow-hidden"
          >
            <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-primary-500/10 to-accent-500/10 rounded-full -translate-y-16 translate-x-16 group-hover:scale-150 transition-transform duration-500"></div>
            <div className={`inline-flex p-4 rounded-2xl ${feature.color} mb-6 relative z-10`}>
              <feature.icon className={`h-8 w-8 ${feature.iconColor}`} />
            </div>
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4 relative z-10">{feature.title}</h3>
            <p className="text-gray-600 dark:text-gray-400 leading-relaxed relative z-10">{feature.description}</p>
          </motion.div>
        ))}
      </div>

      {/* Detection Process Timeline */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="bg-white dark:bg-gray-800 rounded-3xl shadow-xl border border-gray-100 dark:border-gray-700 overflow-hidden"
      >
        <div className="bg-gradient-to-r from-primary-500 to-accent-500 p-8 text-white">
          <div className="flex items-center space-x-4 mb-4">
            <Clock className="h-8 w-8" />
            <h2 className="text-3xl font-bold">Detection Process Timeline</h2>
          </div>
          <p className="text-primary-100 text-lg">
            Follow the journey of your message through our advanced AI-powered analysis pipeline
          </p>
        </div>
        
        <div className="p-8">
          <div className="relative">
            {/* Timeline Line */}
            <div className="absolute left-8 top-0 bottom-0 w-1 bg-gradient-to-b from-primary-500 to-accent-500 rounded-full"></div>
            
            <div className="space-y-12">
              {detectionSteps.map((step, index) => (
                <motion.div
                  key={step.step}
                  initial={{ opacity: 0, x: -50 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.6 + index * 0.1 }}
                  className="relative flex items-start space-x-6"
                >
                  {/* Timeline Node */}
                  <div className={`relative z-10 flex items-center justify-center w-16 h-16 ${step.color} rounded-full shadow-lg`}>
                    <step.icon className="h-8 w-8 text-white" />
                    <div className="absolute -top-2 -right-2 w-6 h-6 bg-white dark:bg-gray-800 rounded-full flex items-center justify-center shadow-md">
                      <span className="text-xs font-bold text-gray-900 dark:text-white">{step.step}</span>
                    </div>
                  </div>
                  
                  {/* Content */}
                  <div className="flex-1 bg-gray-50 dark:bg-gray-700 rounded-2xl p-6 shadow-md">
                    <div className="flex items-center justify-between mb-4">
                      <h4 className="text-xl font-bold text-gray-900 dark:text-white">{step.title}</h4>
                      {index < detectionSteps.length - 1 && (
                        <ArrowRight className="h-5 w-5 text-gray-400" />
                      )}
                    </div>
                    <p className="text-gray-600 dark:text-gray-400 mb-4">{step.description}</p>
                    
                    {/* Details */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                      {step.details.map((detail, detailIndex) => (
                        <motion.div
                          key={detailIndex}
                          initial={{ opacity: 0, scale: 0.9 }}
                          animate={{ opacity: 1, scale: 1 }}
                          transition={{ delay: 0.8 + index * 0.1 + detailIndex * 0.05 }}
                          className="flex items-center space-x-2 text-sm text-gray-500 dark:text-gray-400"
                        >
                          <div className="w-2 h-2 bg-primary-500 rounded-full"></div>
                          <span>{detail}</span>
                        </motion.div>
                      ))}
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </motion.div>

      {/* Spam vs Ham Indicators */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Spam Indicators */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.8 }}
          className="bg-white dark:bg-gray-800 rounded-3xl shadow-xl border border-gray-100 dark:border-gray-700 overflow-hidden"
        >
          <div className="bg-gradient-to-r from-red-500 to-red-600 p-6 text-white">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-white/20 rounded-lg">
                <AlertTriangle className="h-6 w-6" />
              </div>
              <h3 className="text-2xl font-bold">Spam Indicators</h3>
            </div>
          </div>
          <div className="p-6">
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              Common characteristics that indicate a message might be spam:
            </p>
            <div className="space-y-3">
              {spamIndicators.map((indicator, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.9 + index * 0.05 }}
                  className={`flex items-start space-x-3 p-3 rounded-lg border ${getSeverityColor(indicator.severity)}`}
                >
                  <div className="w-2 h-2 bg-current rounded-full mt-2 flex-shrink-0" />
                  <span className="font-medium">{indicator.text}</span>
                </motion.div>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Ham Indicators */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.9 }}
          className="bg-white dark:bg-gray-800 rounded-3xl shadow-xl border border-gray-100 dark:border-gray-700 overflow-hidden"
        >
          <div className="bg-gradient-to-r from-green-500 to-green-600 p-6 text-white">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-white/20 rounded-lg">
                <CheckCircle className="h-6 w-6" />
              </div>
              <h3 className="text-2xl font-bold">Safe Message Indicators</h3>
            </div>
          </div>
          <div className="p-6">
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              Characteristics that suggest a message is legitimate (Ham):
            </p>
            <div className="space-y-3">
              {safeIndicators.map((indicator, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 1.0 + index * 0.05 }}
                  className={`flex items-start space-x-3 p-3 rounded-lg border ${getSeverityColor(indicator.severity)}`}
                >
                  <div className="w-2 h-2 bg-current rounded-full mt-2 flex-shrink-0" />
                  <span className="font-medium">{indicator.text}</span>
                </motion.div>
              ))}
            </div>
          </div>
        </motion.div>
      </div>

      {/* Performance Stats */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1.1 }}
        className="relative overflow-hidden bg-gradient-to-r from-primary-500 via-purple-500 to-accent-500 rounded-3xl shadow-2xl"
      >
        <div className="absolute inset-0 bg-black/10"></div>
        <div className="relative z-10 p-12 text-white">
          <div className="text-center mb-12">
            <h3 className="text-3xl font-bold mb-4">Model Performance Metrics</h3>
            <p className="text-primary-100 text-lg max-w-2xl mx-auto">
              Production-ready instant analysis with confidence scoring
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {[
              { metric: '97.3%', label: 'Overall Accuracy', description: 'Correctly classified messages' },
              { metric: '98.1%', label: 'Spam Detection', description: 'True positive rate' },
              { metric: '96.8%', label: 'Ham Accuracy', description: 'Legitimate message accuracy' },
              { metric: '<50ms', label: 'Processing Time', description: 'Average analysis speed' }
            ].map((stat, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 1.2 + index * 0.1 }}
                className="text-center bg-white/10 backdrop-blur-sm rounded-2xl p-6"
              >
                <div className="text-4xl font-bold mb-2">{stat.metric}</div>
                <div className="text-lg font-semibold mb-1">{stat.label}</div>
                <div className="text-sm text-primary-100">{stat.description}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.div>

      {/* Privacy Notice */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1.3 }}
        className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 border border-blue-200 dark:border-blue-800 rounded-3xl p-8"
      >
        <div className="flex items-start space-x-6">
          <div className="p-3 bg-blue-500 rounded-2xl">
            <Shield className="h-8 w-8 text-white" />
          </div>
          <div>
            <h4 className="text-2xl font-bold text-blue-900 dark:text-blue-300 mb-4">Privacy & Security Commitment</h4>
            <div className="space-y-3 text-blue-800 dark:text-blue-300">
              <p>
                🔒 <strong>End-to-End Security:</strong> Your messages are processed securely and are not stored permanently on our servers.
              </p>
              <p>
                🛡️ <strong>Data Protection:</strong> We prioritize your privacy and only retain analysis results for your personal dashboard.
              </p>
              <p>
                🔐 <strong>Industry Standards:</strong> All communications are encrypted and handled according to industry-standard security practices.
              </p>
              <p>
                ⚡ <strong>Real-time Processing:</strong> Messages are analyzed in real-time without being logged or shared with third parties.
              </p>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Explanation;