"""
Simple backend startup script
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from app import create_app
    
    print("=" * 50)
    print("Starting SMS Guard Backend...")
    print("=" * 50)
    
    app = create_app()
    
    print("✅ Flask app created successfully")
    print("🚀 Starting server on http://localhost:5000")
    print("📊 API endpoints available:")
    print("   - POST /api/auth/login")
    print("   - POST /api/auth/register") 
    print("   - POST /api/predict")
    print("   - GET /api/user/stats")
    print("   - GET /api/health")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
    
except Exception as e:
    print(f"❌ Error starting backend: {str(e)}")
    import traceback
    traceback.print_exc()
