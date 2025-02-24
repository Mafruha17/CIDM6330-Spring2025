from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

DATABASE_URL = "postgresql://WT-mc-student-19425:berti2-peDtyn-duhboj@localhost/student_db"
# ✅ Improved: Enable logging for debugging
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Define Base class (for models)
class Base(DeclarativeBase):
    pass

# ✅ Function to create tables when needed
def create_tables():
    print("Creating tables...")  # ✅ Log message
    Base.metadata.create_all(bind=engine)

# ✅ Dependency to get a database session in FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db  # ✅ Provide DB session
    finally:
        db.close()  # ✅ Ensure it's closed

# ✅ Only create tables when explicitly run
if __name__ == "__main__":
    create_tables()

