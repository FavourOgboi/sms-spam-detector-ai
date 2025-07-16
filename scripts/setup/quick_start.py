#!/usr/bin/env python3
"""
Quick start script to get the backend running
"""

import subprocess
import sys
import os
import time

def install_requirements():
    """Install Python requirements"""
    print("📦 Installing Python requirements...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"], 
                      check=True, cwd=os.getcwd())
        print("✅ Requirements installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def start_backend():
    """Start the backend server"""
    print("🚀 Starting backend server...")
    try:
        # Change to backend directory and run
        os.chdir("backend")
        subprocess.run([sys.executable, "run.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start backend: {e}")
        return False
    except KeyboardInterrupt:
        print("\n⏹️  Backend stopped")
        return True

def main():
    print("🔧 SMS Guard Quick Start")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("backend"):
        print("❌ Backend directory not found. Make sure you're in the project root.")
        return
    
    # Install requirements
    if not install_requirements():
        print("💡 Try running manually: pip install -r backend/requirements.txt")
        return
    
    print("\n🎯 Starting backend server...")
    print("   Demo login: demo / demo123")
    print("   API will be at: http://localhost:5000/api")
    print("   Press Ctrl+C to stop")
    print("=" * 40)
    
    start_backend()

if __name__ == "__main__":
    main()
