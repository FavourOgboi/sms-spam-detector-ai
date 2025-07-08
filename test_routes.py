"""
Test script to verify Flask routes are working
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from app import create_app
    
    app = create_app()
    
    print("✅ Flask app created successfully")
    print("\n📋 Registered routes:")
    
    with app.app_context():
        for rule in app.url_map.iter_rules():
            print(f"   {rule.methods} {rule.rule}")
    
    print(f"\n🚀 Starting test server...")
    
    # Test the health endpoint
    with app.test_client() as client:
        response = client.get('/api/health')
        print(f"\n🧪 Health check test:")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
    
    print(f"\n✅ Routes are working! Starting server on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
