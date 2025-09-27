#!/usr/bin/env python3
"""
Check database and password reset tokens
"""

from backend.app import create_app
from backend.models import db, User, PasswordResetToken

def check_database():
    """Check database tables and tokens"""
    app = create_app()
    
    with app.app_context():
        print("🔍 Database Check")
        print("=" * 30)
        
        # Check if tables exist
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"📊 Tables in database: {tables}")
        
        if 'password_reset_tokens' in tables:
            print("✅ PasswordResetToken table exists")
            
            # Check existing tokens
            tokens = PasswordResetToken.query.all()
            print(f"🎫 Total tokens in database: {len(tokens)}")
            
            for token in tokens:
                print(f"  - Token: {token.token[:20]}...")
                print(f"    User ID: {token.user_id}")
                print(f"    Expiry: {token.expiry}")
                print(f"    Used: {token.used}")
                print(f"    Valid: {token.is_valid()}")
                print()
        else:
            print("❌ PasswordResetToken table missing!")
            print("💡 Run: python backend/create_tables.py")
        
        # Check users
        users = User.query.all()
        print(f"👥 Users in database: {len(users)}")
        for user in users:
            print(f"  - {user.username} ({user.email})")

if __name__ == "__main__":
    check_database()
