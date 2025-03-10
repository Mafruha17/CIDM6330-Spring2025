from pydantic import BaseModel, EmailStr, ConfigDict
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
    """
    Represents a Patient with embedded lists of DeviceSchema and ProviderSchema.
    This is convenient if you want to nest device/provider details in responses.
    """
    id: int
    name: str
    email: EmailStr
    age: int
    active: bool = True
    devices: List[DeviceSchema] = [] 
    providers: List[ProviderSchema] = []

    # For Pydantic v2, ensures we can map a Patient SQLModel instance to this schema.
    model_config = ConfigDict(from_attributes=True)
