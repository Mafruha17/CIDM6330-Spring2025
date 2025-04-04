from __future__ import annotations
from pydantic import EmailStr, Field
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
    devices: Optional[List["DeviceOut"]] = Field(default_factory=list)
    providers: Optional[List["ProviderOut"]] = Field(default_factory=list)

# Runtime imports to resolve forward references
#from .provider_schema import ProviderOut
#from .device_schema import DeviceOut

#PatientOut.model_rebuild()
