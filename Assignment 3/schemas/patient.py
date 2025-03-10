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
    id: int
    name: str
    email: EmailStr
    age: int
    active: bool = True
    devices: List[DeviceSchema] = [] 
    providers: List[ProviderSchema] = []

    model_config = ConfigDict(from_attributes=True)
