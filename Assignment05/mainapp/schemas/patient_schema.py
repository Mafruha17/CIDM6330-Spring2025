from pydantic import EmailStr
from ninja import Schema
from typing import List, Optional
from .device_schema import DeviceOut
from .provider_schema import ProviderOut

class PatientIn(Schema):
    name: str
    email: EmailStr
    age: int
    active: bool = True

class PatientOut(PatientIn):
    id: int
    devices: Optional[List[DeviceOut]] = []
    providers: Optional[List[ProviderOut]] = []
