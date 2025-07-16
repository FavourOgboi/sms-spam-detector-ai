"""
SMS Guard Backend Setup Script

This script automates the setup process for the SMS Guard Flask backend.
It will:
1. Create the ML model
2. Set up the database
3. Create necessary directories
4. Provide instructions for running the backend

Run this script from the project root directory.
"""

import os
import sys
import subprocess
import shutil

def run_command(command, cwd=None):
    """Run a shell command and return success status"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {command}")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {command}")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {command} - Exception: {str(e)}")
        return False

def check_python():
    """Check if Python is available"""
    print("Checking Python installation...")
    if run_command("python --version"):
        return True
    elif run_command("python3 --version"):
        return True
    else:
        print("❌ Python not found. Please install Python 3.7 or higher.")
        return False

def setup_directories():
    """Create necessary directories"""
    print("\nSetting up directories...")
    
    directories = [
        "backend/uploads/profile_images",
        "backend/ml_model/models",
        "ml_notebooks"
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Created directory: {directory}")
        except Exception as e:
            print(f"❌ Failed to create directory {directory}: {str(e)}")

def create_env_file():
    """Create .env file if it doesn't exist"""
    print("\nSetting up environment file...")
    
    env_path = "backend/.env"
    env_example_path = "backend/.env.example"
    
    if not os.path.exists(env_path):
        if os.path.exists(env_example_path):
            try:
                shutil.copy(env_example_path, env_path)
                print(f"✅ Created {env_path} from example")
                print("⚠️  Please edit backend/.env with your configuration")
            except Exception as e:
                print(f"❌ Failed to create .env file: {str(e)}")
        else:
            # Create a basic .env file
            env_content = """# Flask Configuration
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET_KEY=jwt-secret-key-change-in-production

# Database Configuration
DATABASE_URL=sqlite:///smsguard.db

# File Upload Configuration
UPLOAD_FOLDER=uploads/profile_images
MAX_CONTENT_LENGTH=5242880

# CORS Configuration
CORS_ORIGINS=http://localhost:5173
"""
            try:
                with open(env_path, 'w') as f:
                    f.write(env_content)
                print(f"✅ Created basic {env_path}")
            except Exception as e:
                print(f"❌ Failed to create .env file: {str(e)}")
    else:
        print(f"✅ {env_path} already exists")

def install_dependencies():
    """Install Python dependencies"""
    print("\nInstalling Python dependencies...")
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if not in_venv:
        print("⚠️  Warning: Not in a virtual environment")
        print("   It's recommended to create and activate a virtual environment first:")
        print("   python -m venv venv")
        print("   venv\\Scripts\\activate  # On Windows")
        print("   source venv/bin/activate  # On macOS/Linux")
        print()
        
        response = input("Continue anyway? (y/N): ").strip().lower()
        if response != 'y':
            print("Setup cancelled. Please set up a virtual environment first.")
            return False
    
    # Install dependencies
    requirements_path = "backend/requirements.txt"
    if os.path.exists(requirements_path):
        return run_command(f"pip install -r {requirements_path}")
    else:
        print(f"❌ Requirements file not found: {requirements_path}")
        return False

def create_ml_model():
    """Create the machine learning model"""
    print("\nCreating machine learning model...")
    
    model_script = "ml_notebooks/create_spam_model.py"
    if os.path.exists(model_script):
        return run_command(f"python {model_script}")
    else:
        print(f"❌ Model creation script not found: {model_script}")
        return False

def initialize_database():
    """Initialize the database"""
    print("\nInitializing database...")
    
    init_command = 'python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print(\'Database initialized successfully!\')"'
    return run_command(init_command, cwd="backend")

def main():
    """Main setup function"""
    print("=" * 60)
    print("SMS Guard Backend Setup")
    print("=" * 60)
    
    # Check Python
    if not check_python():
        return
    
    # Setup directories
    setup_directories()
    
    # Create .env file
    create_env_file()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies. Please check the error messages above.")
        return
    
    # Create ML model
    if not create_ml_model():
        print("⚠️  ML model creation failed. You can create it manually later.")
        print("   Run: python ml_notebooks/create_spam_model.py")
    
    # Initialize database
    if not initialize_database():
        print("⚠️  Database initialization failed. You can initialize it manually later.")
        print("   Run from backend directory:")
        print('   python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"')
    
    print("\n" + "=" * 60)
    print("Setup completed!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review and edit backend/.env with your configuration")
    print("2. Start the backend server:")
    print("   cd backend")
    print("   python run.py")
    print("3. Test the API:")
    print("   python backend/test_api.py")
    print("\nThe backend will be available at: http://localhost:5000")
    print("API documentation: http://localhost:5000/api/health")
    print("=" * 60)

if __name__ == "__main__":
    main()
