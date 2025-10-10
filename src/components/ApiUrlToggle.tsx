import React from "react";
import { useApiUrl } from "../contexts/ApiUrlContext";

const LOCAL_API_URL = "http://localhost:5000/api";
const DEPLOYED_API_URL = "https://sms-spam-detector-ai.onrender.com/api";

export const ApiUrlToggle: React.FC = () => {
  const { apiUrl, setApiUrl } = useApiUrl();

  return (
    <div style={{
      position: "fixed",
      top: 10,
      right: 10,
      background: "#fff",
      border: "1px solid #ccc",
      borderRadius: 6,
      padding: "6px 12px",
      zIndex: 9999,
      fontSize: 14,
      boxShadow: "0 2px 8px rgba(0,0,0,0.08)"
    }}>
      <label htmlFor="api-url-select" style={{ marginRight: 8, fontWeight: 500 }}>
        API Server:
      </label>
      <select
        id="api-url-select"
        value={apiUrl}
        onChange={e => setApiUrl(e.target.value)}
        style={{ fontSize: 14, padding: "2px 6px" }}
      >
        <option value={LOCAL_API_URL}>Localhost</option>
        <option value={DEPLOYED_API_URL}>Deployed (Render)</option>
      </select>
    </div>
  );
};
