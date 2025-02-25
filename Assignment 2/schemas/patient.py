from pydantic import BaseModel

class PatientSchema(BaseModel):
    id: int
    name: str
    email: str
    age: int | None = None

    class Config:
        from_attributes = True  # Required for SQLAlchemy models