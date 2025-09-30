#!/usr/bin/env python
"""Direct test of backend startup"""
import os
import sys

# Change to backend directory
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
os.chdir(backend_dir)

print(f"Working directory: {os.getcwd()}")
print(f"Files in directory: {os.listdir('.')}")

# Now try to run the app
if __name__ == '__main__':
    try:
        from app import create_app
        print("✅ Successfully imported create_app")
        
        app = create_app()
        print("✅ Successfully created app")
        print("🚀 Starting Flask server on http://0.0.0.0:5000")
        print("=" * 60)
        
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

