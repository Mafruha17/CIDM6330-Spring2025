import os
from sqlmodel import Session, create_engine
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database/database.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

def get_db():
    """Dependency to provide a SQLModel session"""
    with Session(engine) as session:
        print(f"DEBUG: get_db() is yielding {type(session)}")  # 🛠 Debugging line
        yield session
