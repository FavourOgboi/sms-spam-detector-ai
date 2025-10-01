import React, { useState } from "react";
import { motion } from "framer-motion";
import {
  AlertTriangle,
  BarChart3,
  CheckCircle,
  History,
  Lightbulb,
  Send
} from "lucide-react";
import { Link } from "react-router-dom";
import GuardAnimation from "../components/ui/GuardAnimation";
import LoadingSpinner from "../components/ui/LoadingSpinner";
import { predictionService } from "../services/api";
import { EnsemblePredictionResult, PredictionResult } from "../types";

const Predict: React.FC = () => {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [ensembleResult, setEnsembleResult] = useState<EnsemblePredictionResult | null>(null);
  const [error, setError] = useState("");
  const [explanation, setExplanation] = useState<any>(null);
  const [loadingExplanation, setLoadingExplanation] = useState(false);

  const resetForm = () => {
    setMessage("");
    setEnsembleResult(null);
    setExplanation(null);
    setError("");
  };

  const handleExplain = async () => {
    if (!message.trim()) {
      setError("SMS message cannot be empty");
      return;
    }
    setLoadingExplanation(true);
    setError("");
    try {
      const response = await predictionService.explainPrediction(message, 10);
      if (response.success && response.data) {
        setExplanation(response.data);
      } else {
        setError(response.error || "Explanation failed");
      }
    } catch (err) {
      setError("Explanation failed. Please try again.");
    } finally {
      setLoadingExplanation(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim()) {
      setError("SMS message cannot be empty");
      return;
    }
    setLoading(true);
    setError("");
    setEnsembleResult(null);
    setExplanation(null);

    try {
      const response = await predictionService.predictSpam(message);
      console.log("Prediction API response:", response);
        if (response.success && response.data) {
          setEnsembleResult(response.data);
          console.log("EnsembleResult:", response.data);
        } else {
          setError(response.error || "Prediction failed");
        }
    } catch (err) {
      setError("Prediction failed. Please try again.");
      console.error("Prediction error:", err);
    } finally {
      setLoading(false);
    }
  };

  const isFormValid = message.trim().length > 0;

  // Type guard for ensemble result
  function isEnsembleResult(data: any): data is EnsemblePredictionResult {
    return (
      data &&
      typeof data === "object" &&
      "consensus" in data &&
      "model_results" in data &&
      typeof data.model_results === "object"
    );
  }

  // Get the "main" model result for the classic UI (e.g., majority vote model, or first model)
  const mainModelResult: PredictionResult | null =
    ensembleResult && isEnsembleResult(ensembleResult) && Object.values(ensembleResult.model_results).length > 0
      ? Object.values(ensembleResult.model_results)[0]
      : null;

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
          Analyze your SMS messages using our advanced machine learning ensemble. 
          Paste your message below and get instant spam detection results, including consensus and all model votes.
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
                if (error) setError("");
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

            {(ensembleResult || error) && (
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
      {error && (
        <div className="bg-red-100 text-red-700 p-4 rounded-lg border border-red-300">
          <strong>Error:</strong> {error}
        </div>
      )}
      {ensembleResult && !isEnsembleResult(ensembleResult) && (
        <div className="bg-red-100 text-red-700 p-4 rounded-lg border border-red-300">
          <strong>Backend Error:</strong> The backend is returning a single-model result, not the expected ensemble structure.<br />
          Please update your backend <code>/predict</code> endpoint to return <code>{`{ consensus, model_results }`}</code>.<br />
          <pre className="text-xs mt-2">{JSON.stringify(ensembleResult, null, 2)}</pre>
        </div>
      )}
      {console.log("EnsembleResult (render):", ensembleResult)}
      {ensembleResult && isEnsembleResult(ensembleResult) && mainModelResult && (
        <motion.div
          initial={{ opacity: 0, y: 20, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ delay: 0.1 }}
          className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 overflow-hidden"
        >
          {/* Consensus/Final Suggestion */}
          <div className="px-8 py-6 bg-gradient-to-r from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 border-b-2 border-blue-200 dark:border-blue-800">
            <h3 className="text-xl font-bold text-blue-900 dark:text-blue-100 mb-2">
              Final Suggestion (Consensus)
            </h3>
            <div className="flex flex-wrap gap-4 items-center">
              <span className="text-lg font-semibold">
                Majority Vote:{" "}
                <span
                  className={
                    ensembleResult.consensus.majority_vote === "Spam"
                      ? "text-red-600"
                      : "text-green-600"
                  }
                >
                  {ensembleResult.consensus.majority_vote}
                </span>
              </span>
              <span className="text-lg font-semibold">
                Weighted Vote:{" "}
                <span
                  className={
                    ensembleResult.consensus.weighted_vote === "Spam"
                      ? "text-red-600"
                      : "text-green-600"
                  }
                >
                  {ensembleResult.consensus.weighted_vote}
                </span>
              </span>
              <span className="text-sm text-gray-500">
                Spam votes: {ensembleResult.consensus.spam_votes} / {ensembleResult.consensus.total_votes}, Ham votes: {ensembleResult.consensus.ham_votes} / {ensembleResult.consensus.total_votes}
              </span>
            </div>
          </div>

          {/* All Model Results */}
          <div className="p-8 space-y-6">
            <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Individual Model Results
            </h4>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead>
                  <tr>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Model</th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Prediction</th>
                    <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Confidence</th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                  {Object.entries(ensembleResult.model_results).map(
                    ([modelName, modelRes]: [string, PredictionResult]) => (
                      <tr key={modelName}>
                        <td className="px-4 py-2 font-medium text-gray-900 dark:text-white">{modelName}</td>
                        <td className="px-4 py-2">
                          <span
                            className={`px-2 py-1 rounded-full text-xs font-semibold ${
                              modelRes?.prediction === "spam"
                                ? "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300"
                                : "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300"
                            }`}
                          >
                            {modelRes?.prediction ? modelRes.prediction.toUpperCase() : ''}
                          </span>
                        </td>
                        <td className="px-4 py-2">
                          {typeof modelRes.confidence === "number"
                            ? (modelRes.confidence * 100).toFixed(1) + "%"
                            : "N/A"}
                        </td>
                      </tr>
                    )
                  )}
                </tbody>
              </table>
            </div>
          </div>
          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 pt-4 px-8 pb-8">
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
              {loadingExplanation ? "Explaining..." : "Explain Prediction"}
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
                <p className="text-blue-100">Top spam/ham indicator words for this prediction</p>
              </div>
            </div>
          </div>
          <div className="p-8 space-y-6">
            {explanation.summary && (
              <div className="mb-4 text-blue-700 dark:text-blue-300 font-semibold">
                {explanation.summary}
              </div>
            )}
            {explanation.top_features && (
              <div>
                <h4 className="font-medium mb-2">Top Indicator Words:</h4>
                <ul className="list-disc pl-6">
                  {explanation.top_features.map((feat: any, idx: number) => (
                    <li key={idx} className={feat.direction === "spam" ? "text-red-600" : "text-green-600"}>
                      <span className="font-bold">{feat.feature}</span>
                      {" — "}
                      {feat.direction === "spam" ? "Spam indicator" : "Ham indicator"}
                      {typeof feat.importance === "number" && (
                        <> (importance: {feat.importance.toFixed(2)})</>
                      )}
                    </li>
                  ))}
                </ul>
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
            onClick={() => setMessage("Congratulations! You've won $1000! Click here to claim your prize: bit.ly/claim-now")}
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
            onClick={() => setMessage("Hi! Are we still meeting for lunch tomorrow at 1pm? Let me know if you need to reschedule.")}
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
