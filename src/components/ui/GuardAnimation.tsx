import React from 'react';
import { motion } from 'framer-motion';
import { Shield } from 'lucide-react';

interface GuardAnimationProps {
  isAnalyzing: boolean;
  className?: string;
}

const GuardAnimation: React.FC<GuardAnimationProps> = ({ isAnalyzing, className = '' }) => {
  return (
    <motion.div
      className={`flex items-center justify-center ${className}`}
      initial={{ scale: 0.8, opacity: 0 }}
      animate={{ 
        scale: isAnalyzing ? 1 : 0.8, 
        opacity: isAnalyzing ? 1 : 0,
        rotate: isAnalyzing ? 360 : 0
      }}
      transition={{ 
        duration: 0.5,
        rotate: { duration: 2, repeat: isAnalyzing ? Infinity : 0, ease: 'linear' }
      }}
    >
      <div className="relative">
        <motion.div
          className="absolute inset-0 rounded-full bg-primary-500 opacity-20"
          animate={isAnalyzing ? { scale: [1, 1.2, 1] } : {}}
          transition={{ duration: 1.5, repeat: Infinity }}
        />
        <motion.div
          className="relative p-6 bg-primary-500 rounded-full text-white shadow-lg"
          animate={isAnalyzing ? { 
            boxShadow: [
              '0 0 20px rgba(59, 130, 246, 0.5)',
              '0 0 40px rgba(59, 130, 246, 0.8)',
              '0 0 20px rgba(59, 130, 246, 0.5)'
            ]
          } : {}}
          transition={{ duration: 2, repeat: Infinity }}
        >
          <Shield className="h-12 w-12" />
        </motion.div>
      </div>
    </motion.div>
  );
};

export default GuardAnimation;