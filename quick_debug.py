import sys
import os

os.chdir('backend')
sys.path.insert(0, os.getcwd())

print("Testing imports...")
try:
    from app import create_app
    print("✅ Import successful")
    app = create_app()
    print("✅ App created")
    print(f"✅ Starting on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

