import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

# Load environment variables from .env file (if available)
load_dotenv()

# Use environment variable for DATABASE_URL (default to SQLite)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database/database.db")

# Create Engine with correct connection args
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# Create Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# NOTE: If you are using SQLModel for all your models, this Base is optional.
#       You can safely remove or leave it here for future expansions.
class Base(DeclarativeBase):
    pass

# Dependency for FastAPI: Ensures proper session management
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
