"""Check all required imports"""
import sys

print("Checking imports...")
print("=" * 60)

imports_to_check = [
    ('flask', 'Flask'),
    ('flask_sqlalchemy', 'Flask-SQLAlchemy'),
    ('flask_cors', 'Flask-CORS'),
    ('flask_jwt_extended', 'Flask-JWT-Extended'),
    ('flask_mail', 'Flask-Mail'),
    ('werkzeug', 'Werkzeug'),
    ('dotenv', 'python-dotenv'),
    ('sendgrid', 'SendGrid'),
    ('joblib', 'joblib'),
    ('sklearn', 'scikit-learn'),
    ('nltk', 'NLTK'),
    ('lime', 'LIME'),
    ('shap', 'SHAP'),
]

missing = []
for module, name in imports_to_check:
    try:
        __import__(module)
        print(f"✅ {name}")
    except ImportError as e:
        print(f"❌ {name} - {e}")
        missing.append(name)

print("=" * 60)
if missing:
    print(f"\n⚠️  Missing packages: {', '.join(missing)}")
    print("\nTo install missing packages, run:")
    print("pip install sendgrid")
else:
    print("\n✅ All packages are installed!")

print("\nNow testing backend app import...")
print("=" * 60)

import os
os.chdir('backend')

try:
    from app import create_app
    print("✅ Successfully imported create_app")
    
    app = create_app()
    print("✅ Successfully created Flask app")
    print("\n🎉 Backend is ready to run!")
    print("\nTo start the server, run:")
    print("  cd backend")
    print("  python app.py")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

