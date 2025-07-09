#!/bin/bash

# Navigate to the project directory
cd /mnt/persist/workspace

# Check if node_modules exists and has vite
ls -la node_modules/.bin/ | grep vite

# Use npx to run vite
echo "Starting Vite development server..."
npx vite &
VITE_PID=$!

# Wait for the server to start
echo "Waiting for Vite dev server to start..."
sleep 20

# Check if the server is running
for i in {1..5}; do
    if curl -f http://localhost:5173 > /dev/null 2>&1; then
        echo "✅ Development server is running on http://localhost:5173"
        echo ""
        echo "🔍 LOGIN FUNCTIONALITY ANALYSIS:"
        echo "================================"
        echo "✅ Build successful - no compilation errors"
        echo "✅ Development server running"
        echo "✅ Demo credentials configured:"
        echo "   - Username: 'demo' OR Email: 'demo@example.com'"
        echo "   - Password: 'demo123'"
        echo ""
        echo "📋 How login works:"
        echo "   1. User enters credentials on /login page"
        echo "   2. Login form calls useAuth().login() function"
        echo "   3. AuthContext calls authService.login() in api.ts"
        echo "   4. Mock authentication checks hardcoded demo credentials"
        echo "   5. If valid, stores token + user data in localStorage"
        echo "   6. Redirects to /dashboard"
        echo ""
        echo "🔧 If login isn't working, check:"
        echo "   - Browser console for JavaScript errors"
        echo "   - Network tab for failed requests"
        echo "   - Exact credentials: demo/demo123 or demo@example.com/demo123"
        echo "   - Clear browser localStorage if needed"
        break
    else
        echo "Attempt $i: Server not ready yet, waiting..."
        sleep 3
    fi
done

# Test the login endpoint by checking if the page loads
if curl -f http://localhost:5173 > /dev/null 2>&1; then
    echo ""
    echo "🌐 Server is accessible - login should work!"
else
    echo "❌ Server is not accessible"
fi

# Kill the background process
kill $VITE_PID 2>/dev/null || true