import { AnimatePresence, motion } from 'framer-motion';
import {
  AlertTriangle,
  Brain,
  CheckCircle,
  ChevronDown,
  ChevronUp,
  Eye,
  HelpCircle,
  Lightbulb,
  Target
} from 'lucide-react';
import React, { useState } from 'react';

interface ExplanationFeature {
  feature: string;
  importance: number;
  contribution?: number;
  present: boolean;
  explanation: string;
  method?: 'LIME' | 'SHAP' | 'COMBINED' | 'KEYWORD';
  methods?: string[];
}

interface ExplainableAIProps {
  prediction: 'spam' | 'ham';
  confidence: number;
  spamProbability?: number;
  hamProbability?: number;
  explanations: ExplanationFeature[];
  message: string;
}

const ExplainableAI: React.FC<ExplainableAIProps> = ({
  prediction,
  confidence,
  spamProbability = 0,
  hamProbability = 0,
  explanations,
  message
}) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [selectedExplanation, setSelectedExplanation] = useState<number | null>(null);

  const isSpam = prediction === 'spam';
  const primaryColor = isSpam ? 'red' : 'green';
  const secondaryColor = isSpam ? 'yellow' : 'blue';

  // Get overall explanation (usually the first one)
  const overallExplanation = explanations.find(exp => exp.feature === 'overall_assessment') || explanations[0];
  const featureExplanations = explanations.filter(exp => exp.feature !== 'overall_assessment');

  return (
    <div className="space-y-4">
      {/* Main Prediction Card */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className={`p-6 rounded-xl border-2 ${
          isSpam 
            ? 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800' 
            : 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800'
        }`}
      >
        <div className="flex items-start gap-4">
          <div className={`p-3 rounded-full ${
            isSpam ? 'bg-red-100 dark:bg-red-900/30' : 'bg-green-100 dark:bg-green-900/30'
          }`}>
            {isSpam ? (
              <AlertTriangle className="h-6 w-6 text-red-500" />
            ) : (
              <CheckCircle className="h-6 w-6 text-green-500" />
            )}
          </div>
          
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <h3 className={`text-xl font-bold ${
                isSpam ? 'text-red-700 dark:text-red-300' : 'text-green-700 dark:text-green-300'
              }`}>
                {isSpam ? 'SPAM DETECTED' : 'SAFE MESSAGE'}
              </h3>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                isSpam 
                  ? 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300'
                  : 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300'
              }`}>
                {(confidence * 100).toFixed(1)}% Confident
              </span>
            </div>
            
            {/* Overall Explanation */}
            {overallExplanation && (
              <p className="text-gray-700 dark:text-gray-300 mb-4">
                {overallExplanation.explanation}
              </p>
            )}
            
            {/* Probability Bars */}
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className="text-red-600 dark:text-red-400">Spam Probability</span>
                <span className="font-medium">{(spamProbability * 100).toFixed(1)}%</span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${spamProbability * 100}%` }}
                  transition={{ duration: 1, ease: "easeOut" }}
                  className="bg-red-500 h-2 rounded-full"
                />
              </div>
              
              <div className="flex items-center justify-between text-sm">
                <span className="text-green-600 dark:text-green-400">Ham Probability</span>
                <span className="font-medium">{(hamProbability * 100).toFixed(1)}%</span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${hamProbability * 100}%` }}
                  transition={{ duration: 1, ease: "easeOut", delay: 0.2 }}
                  className="bg-green-500 h-2 rounded-full"
                />
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Detailed Explanations */}
      {featureExplanations.length > 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700"
        >
          <button
            type="button"
            onClick={() => setIsExpanded(!isExpanded)}
            className="w-full p-4 flex items-center justify-between text-left hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors rounded-xl"
          >
            <div className="flex items-center gap-3">
              <Brain className="h-5 w-5 text-blue-500" />
              <span className="font-semibold text-gray-900 dark:text-white">
                AI Explanation - Why this decision?
              </span>
              <span className="text-sm text-gray-500 dark:text-gray-400">
                ({featureExplanations.length} factors analyzed)
              </span>
            </div>
            {isExpanded ? (
              <ChevronUp className="h-5 w-5 text-gray-400" />
            ) : (
              <ChevronDown className="h-5 w-5 text-gray-400" />
            )}
          </button>
          
          <AnimatePresence>
            {isExpanded && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.3 }}
                className="border-t border-gray-200 dark:border-gray-700"
              >
                <div className="p-4 space-y-3">
                  {featureExplanations.map((explanation, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className={`p-4 rounded-lg border cursor-pointer transition-all ${
                        selectedExplanation === index
                          ? 'border-blue-300 bg-blue-50 dark:bg-blue-900/20 dark:border-blue-700'
                          : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500'
                      }`}
                      onClick={() => setSelectedExplanation(selectedExplanation === index ? null : index)}
                    >
                      <div className="flex items-start gap-3">
                        <div className="flex-shrink-0">
                          {explanation.present ? (
                            <Target className="h-4 w-4 text-orange-500 mt-0.5" />
                          ) : (
                            <Eye className="h-4 w-4 text-gray-400 mt-0.5" />
                          )}
                        </div>
                        
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1 flex-wrap">
                            <span className="font-medium text-gray-900 dark:text-white">
                              "{explanation.feature}"
                            </span>

                            {/* Method Badge */}
                            {explanation.method && (
                              <span className={`px-2 py-1 text-xs rounded-full font-medium ${
                                explanation.method === 'LIME'
                                  ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300'
                                  : explanation.method === 'SHAP'
                                  ? 'bg-purple-100 dark:bg-purple-900/30 text-purple-800 dark:text-purple-300'
                                  : explanation.method === 'COMBINED'
                                  ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300'
                                  : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400'
                              }`}>
                                {explanation.method}
                              </span>
                            )}

                            {/* Multiple Methods */}
                            {explanation.methods && explanation.methods.length > 1 && (
                              <span className="px-2 py-1 text-xs rounded-full bg-gradient-to-r from-blue-100 to-purple-100 dark:from-blue-900/30 dark:to-purple-900/30 text-gray-800 dark:text-gray-300 font-medium">
                                {explanation.methods.join(' + ')}
                              </span>
                            )}

                            <span className={`px-2 py-1 text-xs rounded-full ${
                              explanation.present
                                ? 'bg-orange-100 dark:bg-orange-900/30 text-orange-800 dark:text-orange-300'
                                : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400'
                            }`}>
                              {explanation.present ? 'Found' : 'Not Found'}
                            </span>

                            <div className="flex items-center gap-1">
                              <span className="text-xs text-gray-500">Importance:</span>
                              <div className="w-16 h-1 bg-gray-200 dark:bg-gray-600 rounded-full">
                                <div
                                  className={`h-1 rounded-full ${
                                    explanation.method === 'LIME' ? 'bg-blue-500' :
                                    explanation.method === 'SHAP' ? 'bg-purple-500' :
                                    explanation.method === 'COMBINED' ? 'bg-green-500' :
                                    'bg-gray-500'
                                  }`}
                                  style={{ width: `${Math.min(explanation.importance * 100, 100)}%` }}
                                />
                              </div>
                              <span className="text-xs text-gray-500 ml-1">
                                {(explanation.importance * 100).toFixed(1)}%
                              </span>
                            </div>
                          </div>
                          
                          <p className="text-sm text-gray-600 dark:text-gray-400">
                            {explanation.explanation}
                          </p>
                          
                          {selectedExplanation === index && (
                            <motion.div
                              initial={{ opacity: 0, height: 0 }}
                              animate={{ opacity: 1, height: 'auto' }}
                              className="mt-3 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800"
                            >
                              <div className="flex items-start gap-2">
                                <Lightbulb className="h-4 w-4 text-blue-500 mt-0.5 flex-shrink-0" />
                                <div className="text-sm text-blue-700 dark:text-blue-300">
                                  <strong>Technical Details:</strong>
                                  <div className="mt-2 space-y-1">
                                    <div>
                                      <strong>Method:</strong> {explanation.method || 'Analysis'}
                                      {explanation.methods && explanation.methods.length > 1 && (
                                        <span className="text-xs ml-1">({explanation.methods.join(', ')})</span>
                                      )}
                                    </div>
                                    <div>
                                      <strong>Importance:</strong> {(explanation.importance * 100).toFixed(1)}%
                                    </div>
                                    {explanation.contribution !== undefined && (
                                      <div>
                                        <strong>Contribution:</strong> {explanation.contribution > 0 ? '+' : ''}{explanation.contribution.toFixed(3)}
                                        <span className="text-xs ml-1">
                                          ({explanation.contribution > 0 ? 'increases' : 'decreases'} spam probability)
                                        </span>
                                      </div>
                                    )}
                                    <div>
                                      <strong>Detection:</strong> {explanation.present
                                        ? `The word "${explanation.feature}" was detected in your message.`
                                        : `The absence of "${explanation.feature}" influenced the prediction.`
                                      }
                                    </div>
                                    {explanation.method === 'LIME' && (
                                      <div className="text-xs text-blue-600 dark:text-blue-400 mt-2 p-2 bg-blue-50 dark:bg-blue-900/20 rounded">
                                        <strong>LIME:</strong> Local Interpretable Model-agnostic Explanations.
                                        This method tests what happens when this feature changes.
                                      </div>
                                    )}
                                    {explanation.method === 'SHAP' && (
                                      <div className="text-xs text-purple-600 dark:text-purple-400 mt-2 p-2 bg-purple-50 dark:bg-purple-900/20 rounded">
                                        <strong>SHAP:</strong> SHapley Additive exPlanations.
                                        This shows the feature's contribution using game theory.
                                      </div>
                                    )}
                                    {explanation.method === 'COMBINED' && (
                                      <div className="text-xs text-green-600 dark:text-green-400 mt-2 p-2 bg-green-50 dark:bg-green-900/20 rounded">
                                        <strong>Combined Analysis:</strong> This feature was identified as important by multiple explanation methods,
                                        making it highly reliable.
                                      </div>
                                    )}
                                  </div>
                                </div>
                              </div>
                            </motion.div>
                          )}
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
                
                {/* Educational Footer */}
                <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-b-xl border-t border-gray-200 dark:border-gray-600">
                  <div className="flex items-start gap-2">
                    <HelpCircle className="h-4 w-4 text-blue-500 mt-0.5 flex-shrink-0" />
                    <div className="text-sm text-gray-600 dark:text-gray-400">
                      <strong>How it works:</strong> Our AI model analyzes your message for patterns learned from thousands of spam and legitimate messages. 
                      Each factor above contributed to the final decision. Click on any factor to learn more about why it's important.
                    </div>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      )}
    </div>
  );
};

export default ExplainableAI;
