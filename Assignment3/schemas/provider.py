from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional

class PatientSchema(BaseModel):
    """
    A simplified Patient schema used for nesting inside ProviderSchema.
    """
    id: int
    name: str
    email: EmailStr
    age: int
    active: bool = True

class ProviderSchema(BaseModel):
    """
    Represents a Provider with embedded list of Patients.
    """
    id: int
    name: str
    email: EmailStr
    specialty: Optional[str] = None
    patients: List[PatientSchema] = []

    model_config = ConfigDict(from_attributes=True)
