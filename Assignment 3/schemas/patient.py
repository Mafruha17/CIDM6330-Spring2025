from pydantic import BaseModel, EmailStr
from typing import List, Optional

class DeviceSchema(BaseModel):
    id: int
    serial_number: str
    active: bool = True

class ProviderSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    specialty: Optional[str] = None

class PatientSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    active: bool = True
    devices: List[DeviceSchema] = []  # ✅ Fix: List of Device objects
    providers: List[ProviderSchema] = []  # ✅ Fix: Many-to-Many relationship

    class Config:
        from_attributes = True  # ✅ Helps SQLAlchemy models map to Pydantic
