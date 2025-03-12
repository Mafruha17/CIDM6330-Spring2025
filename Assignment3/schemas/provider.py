from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional

class PatientSchema(BaseModel):
    id: Optional[int] = None  # Make id optional
    name: str
    email: EmailStr
    age: int
    active: bool = True

class ProviderSchema(BaseModel):
    id: Optional[int] = None  # Make id optional
    name: str
    email: Optional[EmailStr] = None  # Ensure this doesn't break cases where email is missing
    specialty: Optional[str] = None
    patients: Optional[List[PatientSchema]] = None  # Allow it to be null when not needed

    model_config = ConfigDict(from_attributes=True)
