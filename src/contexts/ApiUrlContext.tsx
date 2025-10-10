import React, { createContext, useContext, useState, ReactNode } from "react";

const ENV_API_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8080";

type ApiUrlContextType = {
  apiUrl: string;
  setApiUrl: (url: string) => void;
};

const ApiUrlContext = createContext<ApiUrlContextType>({
  apiUrl: ENV_API_URL,
  setApiUrl: () => {},
});

export const useApiUrl = () => useContext(ApiUrlContext);

export const ApiUrlProvider = ({ children }: { children: ReactNode }) => {
  const [apiUrl, setApiUrl] = useState<string>(ENV_API_URL);
  return (
    <ApiUrlContext.Provider value={{ apiUrl, setApiUrl }}>
      {children}
    </ApiUrlContext.Provider>
  );
};
