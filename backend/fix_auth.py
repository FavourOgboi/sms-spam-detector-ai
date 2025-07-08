"""
Authentication Fix Script

This script fixes common authentication issues:
1. Recreates database tables
2. Creates a test user with known credentials
3. Tests the authentication flow
"""

from app import create_app, db
from models import User
import os

def fix_authentication():
    """Fix authentication issues"""
    
    app = create_app()
    
    with app.app_context():
        print("=" * 50)
        print("SMS Guard Authentication Fix")
        print("=" * 50)
        
        # 1. Recreate database tables
        print("🔄 Recreating database tables...")
        try:
            db.drop_all()
            db.create_all()
            print("✅ Database tables recreated successfully")
        except Exception as e:
            print(f"❌ Failed to recreate tables: {str(e)}")
            return
        
        # 2. Create test users
        print("\n👤 Creating test users...")
        
        test_users = [
            {
                'username': 'demo',
                'email': 'demo@example.com',
                'password': 'demo123'
            },
            {
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123'
            }
        ]
        
        for user_data in test_users:
            try:
                # Check if user already exists
                existing_user = User.query.filter_by(username=user_data['username']).first()
                if existing_user:
                    print(f"⚠️  User {user_data['username']} already exists, skipping...")
                    continue
                
                # Create new user
                user = User(
                    username=user_data['username'],
                    email=user_data['email']
                )
                user.set_password(user_data['password'])
                
                db.session.add(user)
                db.session.commit()
                
                print(f"✅ Created user: {user_data['username']} / {user_data['email']}")
                print(f"   Password: {user_data['password']}")
                
                # Verify password immediately
                if user.check_password(user_data['password']):
                    print(f"   ✅ Password verification successful")
                else:
                    print(f"   ❌ Password verification failed!")
                
            except Exception as e:
                print(f"❌ Failed to create user {user_data['username']}: {str(e)}")
                db.session.rollback()
        
        # 3. Test authentication flow
        print("\n🧪 Testing authentication flow...")
        
        test_credentials = {
            'username': 'demo',
            'password': 'demo123'
        }
        
        # Find user
        user = User.query.filter_by(username=test_credentials['username']).first()
        
        if user:
            print(f"✅ Found user: {user.username}")
            
            # Test password
            if user.check_password(test_credentials['password']):
                print("✅ Password check successful")
                
                # Test user.to_dict()
                try:
                    user_dict = user.to_dict()
                    print("✅ User serialization successful")
                    print(f"   User data: {user_dict}")
                except Exception as e:
                    print(f"❌ User serialization failed: {str(e)}")
                
            else:
                print("❌ Password check failed")
        else:
            print("❌ User not found")
        
        # 4. List all users for verification
        print("\n📋 All users in database:")
        users = User.query.all()
        for user in users:
            print(f"   {user.username} ({user.email}) - Active: {user.is_active}")
        
        print("\n" + "=" * 50)
        print("Authentication fix completed!")
        print("\nYou can now try logging in with:")
        print("Username: demo")
        print("Password: demo123")
        print("OR")
        print("Username: testuser") 
        print("Password: password123")
        print("=" * 50)

if __name__ == "__main__":
    fix_authentication()
