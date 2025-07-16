#!/usr/bin/env python3
"""
Remove demo user from database
"""

import sys
import os

# Add backend to path
sys.path.append('backend')

def remove_demo_user():
    """Remove demo user from database"""
    try:
        from app import create_app
        from models import db, User
        
        app = create_app()
        
        with app.app_context():
            # Find and remove demo user
            demo_user = User.query.filter_by(username='demo').first()
            
            if demo_user:
                print(f"🗑️  Removing demo user: {demo_user.username}")
                db.session.delete(demo_user)
                db.session.commit()
                print("✅ Demo user removed successfully")
            else:
                print("ℹ️  No demo user found in database")
            
            # Show remaining users
            users = User.query.all()
            print(f"\n👥 Users in database: {len(users)}")
            for user in users:
                print(f"   - {user.username} ({user.email})")
            
            if len(users) == 0:
                print("✨ Database is clean - ready for new user registrations!")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧹 Cleaning Demo User")
    print("=" * 30)
    remove_demo_user()
