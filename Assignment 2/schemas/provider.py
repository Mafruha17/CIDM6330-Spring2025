from pydantic import BaseModel, EmailStr
from typing import List, Optional

class PatientSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    active: bool = True

class ProviderSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    specialty: Optional[str] = None
    patients: List[PatientSchema] = []  # ✅ Fix: Many-to-Many relationship

    class Config:
        from_attributes = True
