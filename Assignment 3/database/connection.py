import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

# ✅ Load environment variables from .env file (if available)
load_dotenv()

# ✅ Use environment variable for DATABASE_URL (default to SQLite)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

# ✅ Create Engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})

# ✅ Create Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Use DeclarativeBase (SQLAlchemy 2.0)
class Base(DeclarativeBase):
    pass

# ✅ Dependency for FastAPI: Ensures correct session management
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
