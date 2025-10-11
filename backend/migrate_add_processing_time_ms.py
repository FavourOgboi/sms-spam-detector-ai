"""
Migration script to add missing column to predictions table and ensure 4 users exist in the database.
Run this ONCE on your backend (locally or on Render) to fix schema and user consistency.
"""
from backend.models import db, User
from backend.app import app

# List of required users
required_users = [
    {"username": "test", "email": "test@example.com", "password": "testpass"},
    {"username": "Evidence", "email": "evidenceumukoro005@gmail.com", "password": "evidencepass"},
    {"username": "Ogboi Favour", "email": "ogboifavourifeanyichukwu@gmail.com", "password": "ogboipass"},
    {"username": "demo", "email": "demo@gmail.com", "password": "demopass"},
]

def add_missing_column():
    with app.app_context():
        # Try to add the column if it doesn't exist
        from sqlalchemy import text
        try:
            with db.engine.connect() as conn:
                conn.execute(text('ALTER TABLE predictions ADD COLUMN processing_time_ms INTEGER'))
            print("✅ Added processing_time_ms column to predictions table.")
        except Exception as e:
            msg = str(e)
            if "duplicate column name" in msg or "already exists" in msg or "duplicate" in msg or "exists" in msg:
                print("Column already exists, skipping.")
            elif "no such table" in msg:
                print("Table does not exist. Please ensure migrations are run in correct order.")
            else:
                print(f"Error adding column: {e}")

        # Ensure required users exist
        users_added = False
        for user in required_users:
            existing_email = User.query.filter_by(email=user["email"]).first()
            existing_username = User.query.filter_by(username=user["username"]).first()
            if not existing_email and not existing_username:
                new_user = User(
                    username=user["username"],
                    email=user["email"]
                )
                new_user.set_password(user["password"])
                db.session.add(new_user)
                users_added = True
                print(f"✅ Added user: {user['username']} ({user['email']})")
            else:
                print(f"User already exists: {user['username']} ({user['email']})")
        if users_added:
            try:
                db.session.commit()
                print("✅ Migration and user sync complete.")
            except Exception as e:
                print(f"Error during user commit: {e}")
        else:
            print("No new users added. Migration complete.")

if __name__ == "__main__":
    add_missing_column()
