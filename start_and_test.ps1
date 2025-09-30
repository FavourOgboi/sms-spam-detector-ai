# SMS Guard - Start System and Test Chatbot
Write-Host "🚀 SMS GUARD - STARTING SYSTEM" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

# Kill existing processes
Write-Host "`n🛑 Stopping existing processes..." -ForegroundColor Yellow
Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*sms-spam-detector-ai*" } | Stop-Process -Force
Get-Process -Name "node" -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*sms-spam-detector-ai*" } | Stop-Process -Force
Start-Sleep -Seconds 2

# Start Backend
Write-Host "`n🔧 Starting Backend..." -ForegroundColor Green
$backendJob = Start-Job -ScriptBlock {
    Set-Location "C:\Users\USER\Documents\GitHub\sms-spam-detector-ai\backend"
    python app.py
}
Write-Host "   Backend starting (Job ID: $($backendJob.Id))..." -ForegroundColor Gray

# Wait for backend to start
Write-Host "`n⏳ Waiting for backend to be ready..." -ForegroundColor Yellow
$maxAttempts = 30
$attempt = 0
$backendReady = $false

while ($attempt -lt $maxAttempts -and -not $backendReady) {
    Start-Sleep -Seconds 1
    $attempt++
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:5000/api/health" -Method GET -TimeoutSec 2 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            $backendReady = $true
            Write-Host "   ✅ Backend is ready!" -ForegroundColor Green
        }
    } catch {
        Write-Host "." -NoNewline -ForegroundColor Gray
    }
}

if (-not $backendReady) {
    Write-Host "`n   ❌ Backend failed to start!" -ForegroundColor Red
    Stop-Job $backendJob
    Remove-Job $backendJob
    exit 1
}

# Start Frontend
Write-Host "`n🎨 Starting Frontend..." -ForegroundColor Green
$frontendJob = Start-Job -ScriptBlock {
    Set-Location "C:\Users\USER\Documents\GitHub\sms-spam-detector-ai"
    npm run dev
}
Write-Host "   Frontend starting (Job ID: $($frontendJob.Id))..." -ForegroundColor Gray

# Wait for frontend to start
Write-Host "`n⏳ Waiting for frontend to be ready..." -ForegroundColor Yellow
$maxAttempts = 30
$attempt = 0
$frontendReady = $false

while ($attempt -lt $maxAttempts -and -not $frontendReady) {
    Start-Sleep -Seconds 1
    $attempt++
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:5174" -Method GET -TimeoutSec 2 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            $frontendReady = $true
            Write-Host "   ✅ Frontend is ready!" -ForegroundColor Green
        }
    } catch {
        Write-Host "." -NoNewline -ForegroundColor Gray
    }
}

if (-not $frontendReady) {
    Write-Host "`n   ⚠️ Frontend may still be starting..." -ForegroundColor Yellow
}

# Test the chatbot
Write-Host "`n🤖 Testing Chatbot..." -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
python test_chatbot.py

# Summary
Write-Host "`n" + "=" * 60 -ForegroundColor Cyan
Write-Host "🎯 SYSTEM STATUS" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

if ($backendReady) {
    Write-Host "✅ Backend: RUNNING (http://localhost:5000)" -ForegroundColor Green
} else {
    Write-Host "❌ Backend: NOT RUNNING" -ForegroundColor Red
}

if ($frontendReady) {
    Write-Host "✅ Frontend: RUNNING (http://localhost:5174)" -ForegroundColor Green
} else {
    Write-Host "⚠️ Frontend: STARTING..." -ForegroundColor Yellow
}

Write-Host "`n📋 WHAT'S NEW:" -ForegroundColor Cyan
Write-Host "   🤖 Simple Keyword-Based Chatbot" -ForegroundColor White
Write-Host "      • No complex AI or ML models" -ForegroundColor Gray
Write-Host "      • Fast and reliable responses" -ForegroundColor Gray
Write-Host "      • Helps users understand spam" -ForegroundColor Gray
Write-Host "      • Provides safety tips" -ForegroundColor Gray

Write-Host "`n🌐 HOW TO USE:" -ForegroundColor Cyan
Write-Host "   1. Open: http://localhost:5174" -ForegroundColor White
Write-Host "   2. Login: demo@example.com / demo123" -ForegroundColor White
Write-Host "   3. Click: 'AI Chat' in the navigation" -ForegroundColor White
Write-Host "   4. Try asking:" -ForegroundColor White
Write-Host "      • 'How do I identify spam?'" -ForegroundColor Gray
Write-Host "      • 'What should I do if I receive spam?'" -ForegroundColor Gray
Write-Host "      • 'I got a message about winning a prize'" -ForegroundColor Gray

Write-Host "`n💡 TIP:" -ForegroundColor Yellow
Write-Host "   The chatbot uses keyword matching to provide helpful" -ForegroundColor White
Write-Host "   information about spam detection and safety!" -ForegroundColor White

Write-Host "`n🛑 TO STOP:" -ForegroundColor Red
Write-Host "   Press Ctrl+C or close this window" -ForegroundColor White

Write-Host "`n" + "=" * 60 -ForegroundColor Cyan

# Keep script running
Write-Host "`n⏸️ Press Ctrl+C to stop all services..." -ForegroundColor Yellow
try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
} finally {
    Write-Host "`n🛑 Stopping services..." -ForegroundColor Red
    Stop-Job $backendJob -ErrorAction SilentlyContinue
    Stop-Job $frontendJob -ErrorAction SilentlyContinue
    Remove-Job $backendJob -ErrorAction SilentlyContinue
    Remove-Job $frontendJob -ErrorAction SilentlyContinue
    Write-Host "✅ All services stopped" -ForegroundColor Green
}

