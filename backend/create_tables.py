#!/usr/bin/env python3
"""
Database table creation script for SMS Spam Detector
Creates all necessary tables including the new PasswordResetToken table
"""

from app import create_app
from models import db, User, Prediction, PasswordResetToken

def create_tables():
    """Create all database tables"""
    app = create_app()
    
    with app.app_context():
        print("🔄 Creating database tables...")
        
        # Create all tables
        db.create_all()
        
        print("✅ Database tables created successfully!")
        print("📋 Tables created:")
        print("  - users")
        print("  - predictions") 
        print("  - password_reset_tokens")
        
        # Verify tables exist
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"\n📊 Total tables in database: {len(tables)}")
        for table in tables:
            print(f"  ✓ {table}")

if __name__ == "__main__":
    create_tables()
