from pydantic import BaseModel, EmailStr
from typing import List, Optional

class PatientSchema(BaseModel):
    id: Optional[int] = None  # Make id optional
    name: str
    email: EmailStr
    age: int
    active: bool = True

    class Config:
        orm_mode = True  # Enables serialization from ORM models

class ProviderSchema(BaseModel):
    id: Optional[int] = None  # Make id optional
    name: str
    email: Optional[EmailStr] = None  # Allow null email
    specialty: Optional[str] = None
    patients: Optional[List[PatientSchema]] = None  # Allow it to be null when not needed

    class Config:
        orm_mode = True  # Enables serialization from ORM models
