import React from 'react';
import { motion } from 'framer-motion';
import { Mail, Linkedin, X, MapPin, Phone, Clock, ExternalLink } from 'lucide-react';

const Contact: React.FC = () => {
  const contactMethods = [
    {
      icon: Mail,
      title: 'Email',
      value: 'ogboifavourifeanyichukwu@gmail.com',
      href: 'mailto:ogboifavourifeanyichukwu@gmail.com?subject=Hello from SMS Guard',
      color: 'bg-blue-500',
      description: 'Send me an email directly'
    },
    {
      icon: Linkedin,
      title: 'LinkedIn',
      value: 'Vincent Favour',
      href: 'https://linkedin.com/in/vincent-favour-297433205/',
      color: 'bg-blue-600',
      description: 'Connect with me professionally'
    },
    {
      icon: X,
      title: 'X',
      value: '@OgboiFavour',
      href: 'https://twitter.com/OgboiFavour',
      color: 'bg-sky-500',
      description: 'Follow me for updates and insights'
    }
  ];

  const developerInfo = [
    {
      icon: MapPin,
      title: 'Location',
      value: 'Lagos, Nigeria',
      description: 'Available for remote opportunities worldwide'
    },
    {
      icon: Clock,
      title: 'Response Time',
      value: 'Within 24 hours',
      description: 'I typically respond to messages quickly'
    },
    {
      icon: Phone,
      title: 'Availability',
      value: 'Open to Opportunities',
      description: 'Available for freelance and full-time positions'
    }
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-12 px-2 sm:px-4">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">Get in Touch</h1>
        <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
          Have questions about SMS Guard or want to collaborate? Connect with me through these channels!
        </p>
      </motion.div>

      {/* Developer Introduction */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-gradient-to-r from-primary-500 to-accent-500 rounded-3xl shadow-xl text-white overflow-hidden"
      >
        <div className="p-8 md:p-12">
          <div className="flex flex-col md:flex-row items-center space-y-6 md:space-y-0 md:space-x-8">
            <div className="flex-shrink-0">
              <img
                src="/pres.jpg"
                alt="Ogboi Favour Ifeanyichukwu"
                className="w-32 h-32 rounded-full object-cover border-4 border-white/20 shadow-xl"
              />
            </div>
            <div className="text-center md:text-left">
              <h2 className="text-3xl font-bold mb-4">Ogboi Favour Ifeanyichukwu</h2>
              <p className="text-xl text-primary-100 mb-4">
                Computer Science Graduate & AI Developer
              </p>
              <p className="text-primary-100 leading-relaxed">
                I'm a passionate computer science graduate from Federal University of Petroleum Resources Effurun, 
                specializing in machine learning and web development. SMS Guard represents my commitment to 
                creating practical AI solutions that help people stay safe in our digital world.
              </p>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Contact Methods */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="space-y-8"
      >
        <div>
          <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 text-center">Contact Methods</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {contactMethods.map((method, index) => (
              <motion.a
                key={method.title}
                href={method.href}
                target="_blank"
                rel="noopener noreferrer"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 + index * 0.1 }}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="flex flex-col items-center p-8 bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 hover:shadow-xl transition-all duration-300 group"
              >
                <div className={`p-4 ${method.color} rounded-xl mb-4 group-hover:scale-110 transition-transform duration-300`}>
                  <method.icon className="h-8 w-8 text-white" />
                </div>
                <h4 className="font-semibold text-gray-900 dark:text-white mb-2 text-lg">{method.title}</h4>
                <p className="text-primary-500 font-medium mb-2 text-center">{method.value}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400 text-center">{method.description}</p>
                <ExternalLink className="h-4 w-4 text-gray-400 group-hover:text-primary-500 transition-colors mt-2" />
              </motion.a>
            ))}
          </div>
        </div>
      </motion.div>

      {/* Quick Contact Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 p-8"
      >
        <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 text-center">Quick Contact</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <motion.a
            href="mailto:ogboifavourifeanyichukwu@gmail.com?subject=Job Opportunity - SMS Guard Developer"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="flex items-center justify-center p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg hover:bg-green-100 dark:hover:bg-green-900/30 transition-colors"
          >
            <Mail className="h-5 w-5 text-green-600 mr-3" />
            <span className="text-green-700 dark:text-green-300 font-medium">Email for Job Opportunities</span>
          </motion.a>
          
          <motion.a
            href="mailto:ogboifavourifeanyichukwu@gmail.com?subject=Collaboration Inquiry - SMS Guard"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="flex items-center justify-center p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg hover:bg-blue-100 dark:hover:bg-blue-900/30 transition-colors"
          >
            <Mail className="h-5 w-5 text-blue-600 mr-3" />
            <span className="text-blue-700 dark:text-blue-300 font-medium">Email for Collaboration</span>
          </motion.a>
        </div>
      </motion.div>

      {/* Additional Info */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
        className="space-y-8"
      >
        <div>
          <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 text-center">Additional Information</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {developerInfo.map((info, index) => (
              <motion.div
                key={info.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.7 + index * 0.1 }}
                className="flex flex-col items-center p-6 bg-gray-50 dark:bg-gray-700 rounded-xl text-center"
              >
                <div className="p-3 bg-primary-100 dark:bg-primary-900/30 rounded-lg mb-4">
                  <info.icon className="h-6 w-6 text-primary-500" />
                </div>
                <h4 className="font-semibold text-gray-900 dark:text-white mb-2">{info.title}</h4>
                <p className="text-gray-700 dark:text-gray-300 font-medium mb-1">{info.value}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">{info.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.div>

      {/* Project Information */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
        className="bg-gray-50 dark:bg-gray-800 rounded-3xl p-8 border border-gray-200 dark:border-gray-700"
      >
        <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 text-center">About SMS Guard</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="text-center">
            <div className="w-16 h-16 bg-primary-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-white">AI</span>
            </div>
            <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Machine Learning</h4>
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              Advanced AI algorithms for accurate spam detection
            </p>
          </div>
          <div className="text-center">
            <div className="w-16 h-16 bg-accent-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-white">🛡️</span>
            </div>
            <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Security First</h4>
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              Privacy-focused design with secure message processing
            </p>
          </div>
          <div className="text-center">
            <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-white">⚡</span>
            </div>
            <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Real-time</h4>
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              Instant analysis with confidence scoring
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Contact;
