#!/usr/bin/env python3
"""
Install explainable AI dependencies for SMS Guard
"""
import subprocess
import sys

def install_package(package):
    """Install a Python package"""
    try:
        print(f"Installing {package}...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                      check=True, capture_output=True, text=True)
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def main():
    print("🔍 Installing Explainable AI Dependencies")
    print("=" * 50)
    
    packages = [
        'lime==0.2.0.1',
        'shap==0.42.1'
    ]
    
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print("\n" + "=" * 50)
    if success_count == len(packages):
        print("🎉 All dependencies installed successfully!")
        print("\n✅ Explainable AI is now available!")
        print("🔍 You can now use the 'Explain Prediction' feature")
    else:
        print(f"⚠️ {success_count}/{len(packages)} packages installed")
        print("Some packages failed to install")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
