import React, { useState } from "react";
import { motion } from "framer-motion";
import { History, Lightbulb, Send } from "lucide-react";
import LoadingSpinner from "../components/ui/LoadingSpinner";
import { usePredictionService, useUserService } from "../services/api";
import { EnsemblePredictionResult, PredictionResult } from "../types";
// Simple modal for history
const HistoryModal: React.FC<{
  open: boolean;
  onClose: () => void;
  predictions: PredictionResult[];
}> = ({ open, onClose, predictions }) => {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
      <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-xl max-w-2xl w-full p-6 relative">
        <button onClick={onClose} className="absolute top-3 right-4 text-gray-400 hover:text-gray-700 dark:hover:text-white text-2xl">&times;</button>
        <h2 className="text-xl font-bold mb-4 text-center">Prediction History</h2>
        {predictions.length === 0 ? (
          <div className="text-center text-gray-500">No predictions yet.</div>
        ) : (
          <div className="max-h-96 overflow-y-auto divide-y divide-gray-200 dark:divide-gray-700">
            {predictions.map((p) => (
              <div key={p.id} className="py-3">
                <div className="flex justify-between items-center">
                  <span className="truncate max-w-xs text-gray-900 dark:text-white">{p.message.slice(0, 60)}{p.message.length > 60 ? '...' : ''}</span>
                  <span className={`ml-2 px-2 py-1 rounded text-xs font-semibold ${p.prediction === 'spam' ? 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300' : 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300'}`}>{p.prediction.toUpperCase()}</span>
                  <span className="ml-2 text-xs text-gray-500">{(p.confidence * 100).toFixed(1)}%</span>
                </div>
                <div className="text-xs text-gray-400 mt-1">{new Date(p.timestamp).toLocaleString()}</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

const Predict: React.FC = () => {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [ensembleResult, setEnsembleResult] = useState<EnsemblePredictionResult | null>(null);
  const [error, setError] = useState("");
  const [explanation, setExplanation] = useState<any>(null);
  const [loadingExplanation, setLoadingExplanation] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [history, setHistory] = useState<PredictionResult[]>([]);
  const [loadingHistory, setLoadingHistory] = useState(false);

  const { predictSpam, explainPrediction } = usePredictionService();
  const { getUserPredictions } = useUserService();

  // Fetch history when modal opens
  const handleOpenHistory = async () => {
    setShowHistory(true);
    setLoadingHistory(true);
    try {
      const res = await getUserPredictions();
      if (res.success && res.data) setHistory(res.data.slice(0, 20));
      else setHistory([]);
    } catch {
      setHistory([]);
    } finally {
      setLoadingHistory(false);
    }
  };

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
      const response = await explainPrediction(message, 10);
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
      const response = await predictSpam(message);
      if (response.success && response.data) {
        setEnsembleResult(response.data);
      } else {
        setError(response.error || "Prediction failed");
      }
    } catch (err) {
      setError("Prediction failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  function isEnsembleResult(data: any): data is EnsemblePredictionResult {
    return (
      data &&
      typeof data === "object" &&
      "consensus" in data &&
      typeof data.consensus === "object" &&
      "model_results" in data &&
      typeof data.model_results === "object" &&
      "weighted_result" in data &&
      typeof data.weighted_result === "object" &&
      "confidence_level" in data &&
      "suggestion" in data &&
      "message" in data
    );
  }

  const isFormValid = message.trim().length > 0;

  return (
    <div className="max-w-4xl mx-auto space-y-8 px-2 sm:px-4">
      {/* Explanation Results - always at the very top */}
      {explanation && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.05 }}
          className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 overflow-hidden mb-8 mt-4"
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

      {/* Prediction Form */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 p-8"
      >
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="sms-message" className="block text-lg font-medium text-gray-900 dark:text-white mb-2">
              Enter SMS Message
            </label>
            <textarea
              id="sms-message"
              className="w-full p-4 rounded-lg border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500 resize-none min-h-[100px]"
              placeholder="Paste or type your SMS message here..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              disabled={loading}
              required
            />
          </div>
          <div className="flex flex-wrap gap-3 justify-end">
            <button
              type="submit"
              disabled={!isFormValid || loading}
              className="flex items-center px-6 py-3 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 transition-all disabled:opacity-50"
            >
              {loading ? <LoadingSpinner size="sm" className="mr-2" /> : <Send className="h-5 w-5 mr-2" />}
              Predict
            </button>
            <button
              type="button"
              onClick={resetForm}
              disabled={loading}
              className="flex items-center px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg font-medium hover:bg-gray-200 dark:hover:bg-gray-600 transition-all disabled:opacity-50"
            >
              Reset
            </button>
          </div>
        </form>
      </motion.div>

      {/* Results & Actions */}
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
      {ensembleResult && isEnsembleResult(ensembleResult) && (
        <motion.div
          initial={{ opacity: 0, y: 20, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ delay: 0.1 }}
          className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 overflow-hidden"
        >
          {/* Action Buttons */}
          <div className="flex flex-wrap gap-3 justify-end p-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/40">
            <button
              type="button"
              onClick={handleOpenHistory}
              className="flex items-center px-4 py-2 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 rounded-lg font-medium hover:bg-primary-200 dark:hover:bg-primary-800 transition-all"
            >
              <History className="h-5 w-5 mr-2" />
              History
            </button>
            <button
              type="button"
              onClick={handleExplain}
              disabled={loadingExplanation || !ensembleResult}
              className="flex items-center px-4 py-2 bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300 rounded-lg font-medium hover:bg-yellow-200 dark:hover:bg-yellow-800 transition-all disabled:opacity-50"
            >
              {loadingExplanation ? <LoadingSpinner size="sm" className="mr-2" /> : <Lightbulb className="h-5 w-5 mr-2" />}
              Explain
            </button>
          </div>

          {/* Header */}
          <div className="p-6 bg-gray-50 dark:bg-gray-900/40 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-2xl font-bold text-center text-gray-800 dark:text-white">
              📩 SMS Spam Detection Result
            </h2>
          </div>

          {/* Message & Final Suggestion */}
          <div className="p-8 space-y-6">
            <div>
              <p className="text-sm text-gray-500 dark:text-gray-400 mb-2">Message:</p>
              <p className="text-gray-800 dark:text-white bg-gray-100 dark:bg-gray-700 p-4 rounded-lg">
                "{ensembleResult.message}"
              </p>
            </div>

            <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Final Suggestion:</h3>
              <div className="space-y-2 text-gray-700 dark:text-gray-300">
                <p>
                  - Consensus (Majority Vote):{" "}
                  <span className={`font-bold ${ensembleResult.consensus.majority_vote.toLowerCase() === 'spam' ? 'text-red-500' : 'text-green-500'}`}>
                    {ensembleResult.consensus.majority_vote.toUpperCase()}
                  </span>
                  ({ensembleResult.consensus.spam_votes}/{ensembleResult.consensus.total_votes} models)
                </p>
                <p>
                  - Weighted Vote (by F1 score):{" "}
                  <span className={`font-bold ${ensembleResult.weighted_result.weighted_majority.toLowerCase() === 'spam' ? 'text-red-500' : 'text-green-500'}`}>
                    {ensembleResult.weighted_result.weighted_majority.toUpperCase()}
                  </span>
                  ({ensembleResult.weighted_result.weighted_spam_prob !== null ? (ensembleResult.weighted_result.weighted_spam_prob * 100).toFixed(1) + "%" : "N/A"} confidence)
                </p>
              </div>
            </div>

            <div className="text-center pt-4">
              <p className="text-lg font-bold">
                Overall Confidence: {" "}
                <span className="text-primary-500">{ensembleResult.confidence_level}</span>
              </p>
              <p className="text-gray-600 dark:text-gray-400 mt-2">{ensembleResult.suggestion}</p>
            </div>
          </div>

          {/* Divider */}
          <div className="border-t border-gray-200 dark:border-gray-700 mx-8"></div>

          {/* Individual Model Results */}
          <div className="p-8">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 text-center">
              Individual Model Results
            </h3>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead className="bg-gray-50 dark:bg-gray-700">
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
                        <td className="px-4 py-2 text-gray-700 dark:text-gray-300">
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
            <p className="text-center text-sm text-gray-500 mt-4">
              Spam Votes: {ensembleResult.consensus.spam_votes} | Ham Votes: {ensembleResult.consensus.ham_votes}
            </p>
          </div>
        </motion.div>
      )}

      {/* History Modal */}
      <HistoryModal open={showHistory} onClose={() => setShowHistory(false)} predictions={history} />
      {showHistory && loadingHistory && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
          <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-xl max-w-xs w-full p-6 text-center">
            <LoadingSpinner size="md" />
            <div className="mt-4 text-gray-700 dark:text-gray-200">Loading history...</div>
          </div>
        </div>
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
