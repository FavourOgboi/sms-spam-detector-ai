@echo off
title SMS Guard Launcher
color 0A
echo.
echo  ███████╗███╗   ███╗███████╗     ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗
echo  ██╔════╝████╗ ████║██╔════╝    ██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗
echo  ███████╗██╔████╔██║███████╗    ██║  ███╗██║   ██║███████║██████╔╝██║  ██║
echo  ╚════██║██║╚██╔╝██║╚════██║    ██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║
echo  ███████║██║ ╚═╝ ██║███████║    ╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝
echo  ╚══════╝╚═╝     ╚═╝╚══════╝     ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝
echo.
echo                         🚀 SMS Guard Launcher 🚀
echo                        ========================
echo.

echo [1/4] 📊 Starting Backend API...
start "SMS Guard Backend" cmd /k "title SMS Guard Backend && cd /d %~dp0 && echo Starting backend... && python fixed_backend.py"

echo [2/4] ⏳ Waiting for backend to initialize...
timeout /t 6 /nobreak >nul

echo [3/4] 🎨 Starting Frontend...
start "SMS Guard Frontend" cmd /k "title SMS Guard Frontend && cd /d %~dp0 && echo Starting frontend... && npm run dev"

echo [4/4] ⏳ Waiting for frontend to start...
timeout /t 10 /nobreak >nul

echo 🌐 Opening SMS Guard in browser...
start http://localhost:5173

echo.
echo ✅ SMS Guard is now running!
echo.
echo 📋 Your Services:
echo   🔧 Backend API:  http://localhost:5000
echo   🎨 Frontend App: http://localhost:5173
echo   🔑 Demo Login:   demo / demo123
echo.
echo 🎯 Features Available:
echo   • Spam Detection with Explainable AI
echo   • User Dashboard and Analytics
echo   • Prediction History
echo   • Profile Management
echo.
echo 🛑 To stop services: Close the terminal windows
echo    or press Ctrl+C in each window
echo.
echo 🎉 Enjoy your SMS Guard system!
echo.
pause
