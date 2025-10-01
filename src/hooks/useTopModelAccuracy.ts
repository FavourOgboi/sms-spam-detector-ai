import { useEffect, useState } from "react";
import api from "../services/api";

export function useTopModelAccuracy(modelResults: any) {
  const [topModel, setTopModel] = useState<{ name: string; accuracy: number } | null>(null);

  useEffect(() => {
    async function fetchAccuracy() {
      if (!modelResults) {
        setTopModel(null);
        return;
      }
      // Find the model with the highest confidence
      let top = { name: "", confidence: -1 };
      Object.entries(modelResults).forEach(([name, res]: [string, any]) => {
        if (typeof res.confidence === "number" && res.confidence > top.confidence) {
          top = { name, confidence: res.confidence };
        }
      });
      if (top.name) {
        // Fetch per-model metrics from backend
        try {
          const response = await api.get("/model/metrics");
          if (response.data.success && response.data.data && response.data.data[top.name]) {
            setTopModel({ name: top.name, accuracy: response.data.data[top.name].accuracy });
          } else {
            setTopModel(null);
          }
        } catch {
          setTopModel(null);
        }
      } else {
        setTopModel(null);
      }
    }
    fetchAccuracy();
  }, [modelResults]);

  return topModel;
}
