import os
import sqlite3
from sqlmodel import SQLModel
from database.connection import engine
from database.models import Device, Patient, Provider, PatientProviderLink

# Define the database file path inside the database folder
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "database.db")


def create_tables():
    """Creates database tables using SQLModel."""
    print("\n🚀 Creating database tables...")

    try:
        # Drop existing tables (CAUTION: This will delete all data!)
        SQLModel.metadata.drop_all(bind=engine)
        print("🗑️ Dropped existing tables!")

        # Create tables with updated schema
        SQLModel.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")

    except Exception as e:
        print(f"❌ Error creating tables: {e}")


def verify_tables():
    """Verifies if tables exist in the SQLite database."""
    print("\n🔍 Verifying existing tables in database.db...")

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()

        if tables:
            print(f"✅ Existing tables: {[table[0] for table in tables]}")
        else:
            print("⚠️ No tables found in the database.")

    except sqlite3.Error as e:
        print(f"❌ SQLite error: {e}")


if __name__ == "__main__":
    # Ensure the database directory exists
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

    # Remove old database file before recreating it
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
        print("🗑️ Old database file removed.")

    create_tables()
    verify_tables()
