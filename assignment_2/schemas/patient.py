from pydantic import BaseModel

# ✅ Schema for creating a new patient (no ID)
class PatientCreate(BaseModel):
    name: str
    email: str
    age: int | None = None  # Optional field

# ✅ Schema for API responses (includes ID)
class PatientSchema(PatientCreate):
    id: int  # ID should only be included in the response

    class Config:
        from_attributes = True  # ✅ Required for SQLAlchemy models
