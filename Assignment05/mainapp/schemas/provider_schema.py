from pydantic import EmailStr
from ninja import Schema
from typing import List, Optional
from .patient_schema import PatientOut

class ProviderIn(Schema):
    name: str
    email: Optional[EmailStr] = None
    specialty: Optional[str] = None

class ProviderOut(ProviderIn):
    id: int
    patients: Optional[List[PatientOut]] = []