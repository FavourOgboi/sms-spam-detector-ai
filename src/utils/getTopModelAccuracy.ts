import api from "../services/api";

/**
 * Given model_results from a prediction, fetch per-model accuracy and return the model with the highest confidence and its accuracy.
 * @param modelResults The model_results object from a prediction
 * @returns {Promise<{ name: string; accuracy: number } | null>}
 */
export async function getTopModelAccuracy(modelResults: any): Promise<{ name: string; accuracy: number } | null> {
  if (!modelResults) return null;
  // Find the model with the highest confidence
  let top = { name: "", confidence: -1 };
  Object.entries(modelResults).forEach(([name, res]: [string, any]) => {
    if (typeof res.confidence === "number" && res.confidence > top.confidence) {
      top = { name, confidence: res.confidence };
    }
  });
  if (top.name) {
    try {
      const response = await api.get("/model/metrics");
      if (response.data.success && response.data.data && response.data.data[top.name]) {
        return { name: top.name, accuracy: response.data.data[top.name].accuracy };
      }
    } catch {
      return null;
    }
  }
  return null;
}
