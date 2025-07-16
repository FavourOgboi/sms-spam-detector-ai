@echo off
echo 🎯 SMS Guard - Complete Setup and Start
echo ========================================

echo 📦 Installing Python dependencies...
pip install flask flask-sqlalchemy flask-cors flask-jwt-extended werkzeug python-dotenv

echo 📦 Installing Node.js dependencies...
npm install

echo 🚀 Starting both Backend and Frontend...
echo ========================================
echo 🔥 Backend will start on: http://localhost:5000
echo ⚡ Frontend will start on: http://localhost:5173
echo 🔑 Demo login: demo / demo123
echo ========================================
echo Press Ctrl+C to stop both servers
echo ========================================

npm run dev

pause
