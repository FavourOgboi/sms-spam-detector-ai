#!/usr/bin/env python3
"""
Install LIME for explainable AI
"""
import subprocess
import sys

def install_lime():
    """Install LIME package"""
    try:
        print("📦 Installing LIME for explainable AI...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'lime'], 
                      check=True, capture_output=True, text=True)
        print("✅ LIME installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install LIME: {e}")
        return False

def test_lime():
    """Test LIME installation"""
    try:
        import lime
        import lime.lime_text
        print("✅ LIME is working correctly!")
        return True
    except ImportError as e:
        print(f"❌ LIME import failed: {e}")
        return False

def main():
    print("🔍 LIME Installation for SMS Guard")
    print("=" * 40)
    
    if install_lime():
        if test_lime():
            print("\n🎉 LIME is ready!")
            print("✅ Explainable AI will now use LIME")
            print("🔄 Restart your backend to enable LIME")
        else:
            print("\n⚠️ LIME installed but not working")
    else:
        print("\n❌ LIME installation failed")
        print("💡 Try: pip install lime")
    
    print("=" * 40)

if __name__ == "__main__":
    main()
