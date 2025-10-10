#!/usr/bin/env powershell

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SMS Spam Detector - Starting Dev Environment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Starting Backend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; python -m app" -WindowStyle Normal

Write-Host "Waiting 8 seconds for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

Write-Host "Starting Frontend Server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run dev:frontend-only" -WindowStyle Normal

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Both servers are starting!" -ForegroundColor Green
Write-Host "  Backend: http://localhost:5000" -ForegroundColor Yellow
Write-Host "  Frontend: http://localhost:5173 (or next available port)" -ForegroundColor Green
Write-Host "  Health Check: http://localhost:5000/api/health" -ForegroundColor Blue
Write-Host ""
Write-Host "🧪 To test the application:" -ForegroundColor Magenta
Write-Host "  1. Go to frontend URL above" -ForegroundColor White
Write-Host "  2. Register a new account or login" -ForegroundColor White
Write-Host "  3. Test SMS spam detection features" -ForegroundColor White
Write-Host "  4. Explore dashboard and user profile" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
