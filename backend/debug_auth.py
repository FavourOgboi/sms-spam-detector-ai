"""
Authentication Debug Script for SMS Guard

This script helps debug authentication issues by:
1. Checking database connection
2. Listing all users
3. Testing password hashing
4. Verifying user credentials
"""

from app import create_app, db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

def debug_authentication():
    """Debug authentication issues"""
    
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("SMS Guard Authentication Debug")
        print("=" * 60)
        
        # 1. Check database connection
        try:
            db.create_all()
            print("✅ Database connection successful")
        except Exception as e:
            print(f"❌ Database connection failed: {str(e)}")
            return
        
        # 2. List all users
        print("\n📋 Current Users in Database:")
        print("-" * 40)
        users = User.query.all()
        
        if not users:
            print("No users found in database")
        else:
            for user in users:
                print(f"ID: {user.id}")
                print(f"Username: {user.username}")
                print(f"Email: {user.email}")
                print(f"Active: {user.is_active}")
                print(f"Password Hash: {user.password_hash[:20]}...")
                print("-" * 40)
        
        # 3. Test password hashing
        print("\n🔐 Testing Password Hashing:")
        test_password = "password123"
        hash1 = generate_password_hash(test_password)
        hash2 = generate_password_hash(test_password)
        
        print(f"Original password: {test_password}")
        print(f"Hash 1: {hash1}")
        print(f"Hash 2: {hash2}")
        print(f"Hashes are different (good): {hash1 != hash2}")
        print(f"Hash 1 verifies: {check_password_hash(hash1, test_password)}")
        print(f"Hash 2 verifies: {check_password_hash(hash2, test_password)}")
        print(f"Wrong password fails: {check_password_hash(hash1, 'wrongpassword')}")
        
        # 4. Interactive user testing
        print("\n🧪 Interactive User Testing:")
        print("Enter credentials to test:")
        
        username_or_email = input("Username or Email: ").strip()
        password = input("Password: ").strip()
        
        if not username_or_email or not password:
            print("❌ Please provide both username/email and password")
            return
        
        # Find user
        user = None
        if '@' in username_or_email:
            user = User.query.filter_by(email=username_or_email.lower()).first()
            print(f"🔍 Searching by email: {username_or_email.lower()}")
        else:
            user = User.query.filter_by(username=username_or_email).first()
            print(f"🔍 Searching by username: {username_or_email}")
        
        if not user:
            print("❌ User not found in database")
            
            # Offer to create user
            create_user = input("\nWould you like to create this user? (y/N): ").strip().lower()
            if create_user == 'y':
                if '@' not in username_or_email:
                    email = input("Enter email for new user: ").strip().lower()
                else:
                    email = username_or_email.lower()
                    username_or_email = input("Enter username for new user: ").strip()
                
                try:
                    new_user = User(username=username_or_email, email=email)
                    new_user.set_password(password)
                    db.session.add(new_user)
                    db.session.commit()
                    print(f"✅ User created successfully!")
                    print(f"   ID: {new_user.id}")
                    print(f"   Username: {new_user.username}")
                    print(f"   Email: {new_user.email}")
                except Exception as e:
                    print(f"❌ Failed to create user: {str(e)}")
                    db.session.rollback()
            return
        
        print(f"✅ User found:")
        print(f"   ID: {user.id}")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Active: {user.is_active}")
        
        # Test password
        password_correct = user.check_password(password)
        print(f"\n🔑 Password Check:")
        print(f"   Password provided: {password}")
        print(f"   Password correct: {password_correct}")
        
        if not password_correct:
            print("❌ Password verification failed!")
            
            # Offer to reset password
            reset_password = input("\nWould you like to reset the password? (y/N): ").strip().lower()
            if reset_password == 'y':
                new_password = input("Enter new password: ").strip()
                if new_password:
                    try:
                        user.set_password(new_password)
                        db.session.commit()
                        print("✅ Password reset successfully!")
                        
                        # Test new password
                        if user.check_password(new_password):
                            print("✅ New password verification successful!")
                        else:
                            print("❌ New password verification failed!")
                    except Exception as e:
                        print(f"❌ Failed to reset password: {str(e)}")
                        db.session.rollback()
        else:
            print("✅ Password verification successful!")
            
            if not user.is_active:
                print("⚠️  User account is inactive!")
                activate = input("Activate account? (y/N): ").strip().lower()
                if activate == 'y':
                    user.is_active = True
                    db.session.commit()
                    print("✅ Account activated!")
        
        print("\n" + "=" * 60)
        print("Debug session completed!")
        print("=" * 60)

if __name__ == "__main__":
    debug_authentication()
