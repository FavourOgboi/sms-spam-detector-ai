# SMS Guard: AI-Powered SMS Spam Detection

## Overview

SMS Guard is a full-stack, production-ready SMS spam detection system built with:
- **Frontend:** React (Vite) for a modern, responsive UI
- **Backend:** Flask (Python) with an ensemble of classic machine learning models (Random Forest, Naive Bayes, etc.)
- **ML Approach:** Ensemble voting, confidence scoring, and explainable AI (LIME/Naive Bayes features)
- **Deployment:** Ready for Fly.io (backend and frontend), Netlify (frontend), or any cloud platform

---

## Features

- **Ensemble Machine Learning:** Multiple classic ML models (Random Forest, Naive Bayes, etc.) analyze each message. Each model votes "spam" or "ham" and provides a confidence score.
- **Consensus Decision:** The final result is based on the majority vote, but also considers how confident the models are and how much they agree.
- **Dynamic Confidence Score:** Combines model agreement and average confidence. If models are split or not confident, the overall confidence is lower.
- **Explainable AI:** Click "Explain Prediction" to see the top spam/ham indicator words for your message, powered by LIME or Naive Bayes.
- **User Guide:** Clear rules and tips for interpreting results, including what to do with low-confidence predictions.
- **Privacy & Security:** Messages are processed securely, not stored permanently, and all communications are encrypted.

---

## How SMS Guard Works

1. **Message Input:** User submits an SMS message for analysis.
2. **Text Preprocessing:** The message is cleaned, tokenized, and prepared for feature extraction (removes special characters, lowercases, tokenizes, removes stop words).
3. **Feature Extraction:** Key linguistic features and patterns are identified (n-gram analysis, keyword detection, URL pattern matching, etc.).
4. **Ensemble Model Analysis:** Multiple ML models process the features and vote on spam/ham, each with a confidence score.
5. **Consensus & Confidence:** The system calculates the majority vote and a consensus confidence score (agreement * average confidence of majority-vote models).
6. **Result Generation:** The app displays the final classification, confidence, and a detailed explanation of the top indicator words.

---

## Model Performance Metrics

- **Accuracy:** Percentage of all messages correctly classified (e.g., 98.2%).
- **Spam Precision:** Of all messages flagged as spam, how many were actually spam (e.g., 99.2%).
- **Ham Accuracy:** Of all legitimate messages, how many were correctly identified as ham (e.g., 98.1%).
- **Processing Time:** Average analysis speed (e.g., <50ms).

---

## User Guide: How to Interpret Results

- **High Confidence (e.g., >80%):** The system is very sure. If it says "spam," be cautious; if it says "ham," it's likely safe.
- **Low Confidence (e.g., <60%):** The models are unsure or split. Use your judgment, especially if the message contains suspicious links or urgent language.
- **Spam Indicators:** Words like "urgent," "prize," "free," or "click" are common spam signals.
- **Ham Indicators:** Words like "meeting," "thanks," or names of known contacts are signs of a legitimate message.
- **If in Doubt:** Do not click links or provide personal information. When confidence is low, treat the message with extra caution.

---

## Privacy & Security

- **End-to-End Security:** Your messages are processed securely and are not stored permanently on our servers.
- **Data Protection:** Only analysis results are retained for your personal dashboard.
- **Industry Standards:** All communications are encrypted and handled according to best practices.
- **Real-time Processing:** Messages are analyzed in real-time without being logged or shared with third parties.

---

## Project Structure

- `src/` — React frontend (Vite)
- `backend/` — Flask backend (API, ML models)
- `ml_notebooks/` — Jupyter notebooks and training scripts
- `models/` — (Legacy) model files
- `public/` — Static assets for frontend
- `uploads/` — User-uploaded files (profile images, etc.)

---

## Environment Variables

- **Backend:**
  - `SECRET_KEY` — Flask secret key
  - `DATABASE_URL` — SQLAlchemy database URI
  - `SENDGRID_API_KEY` — For email sending (optional)
  - `FLASK_ENV` — Set to "production" for deployment
- **Frontend:**
  - `VITE_API_BASE_URL` — URL of the backend API (e.g., https://your-backend.fly.dev/api)

---

## Deployment

See [FLY_DEPLOYMENT.md](FLY_DEPLOYMENT.md) for full instructions on deploying both backend and frontend on Fly.io.

---

## Credits

- Built by Favour Ogboi and contributors.
- Open source libraries: Flask, scikit-learn, React, Vite, LIME, and more.
