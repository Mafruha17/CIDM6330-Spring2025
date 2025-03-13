from pydantic import BaseModel, EmailStr
from typing import List, Optional

class DeviceSchema(BaseModel):
    id: Optional[int] = None  # Make id optional
    serial_number: str
    active: bool = True

    class Config:
        orm_mode = True  # Enables conversion from ORM models

class ProviderSchema(BaseModel):
    id: Optional[int] = None  # Make id optional
    name: str
    email: EmailStr
    specialty: Optional[str] = None

    class Config:
        orm_mode = True  # Enables conversion from ORM models

class PatientSchema(BaseModel):
    """
    Represents a Patient with embedded lists of DeviceSchema and ProviderSchema.
    This is convenient if you want to nest device/provider details in responses.
    """
    id: Optional[int] = None  # Make id optional
    name: str
    email: EmailStr
    age: int
    active: bool = True
    devices: Optional[List[DeviceSchema]] = []  # Make it optional
    providers: Optional[List[ProviderSchema]] = []  # Make it optional

    class Config:
        orm_mode = True  # Enables conversion from ORM models
