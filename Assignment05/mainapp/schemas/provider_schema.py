from __future__ import annotations
from pydantic import EmailStr, Field
from ninja import Schema
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .patient_schema import PatientOut  # Only for type checking

class ProviderIn(Schema):
    name: str
    email: Optional[EmailStr] = None
    specialty: Optional[str] = None

class ProviderOut(ProviderIn):
    id: int
    patients: Optional[List["PatientOut"]] = Field(default_factory=list)

# Runtime import to resolve forward references
#from .patient_schema import PatientOut

#ProviderOut.model_rebuild()
