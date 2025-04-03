from pydantic import EmailStr
from ninja import Schema
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .provider_schema import ProviderOut
    from .device_schema import DeviceOut

class PatientIn(Schema):
    name: str
    email: EmailStr
    age: int
    active: bool = True

class PatientOut(PatientIn):
    id: int
    devices: Optional[List["DeviceOut"]] = []  # ✅ string reference
    providers: Optional[List["ProviderOut"]] = []  # ✅ string reference
