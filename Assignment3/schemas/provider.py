from pydantic import BaseModel, EmailStr,Field
from typing import List, Optional

class PatientSchema(BaseModel):
    id: Optional[int] = None  # Make id optional
    name: str
    email: EmailStr
    age: int
    active: bool = True

    class Config:
        from_attributes = True  # ✅ Fixed for Pydantic v2

class ProviderSchema(BaseModel):
    id: Optional[int] = None  # Make id optional
    name: str
    email: Optional[EmailStr] = None  # Allow null email
    specialty: Optional[str] = None
    patients: Optional[List[PatientSchema]] = []  # Allow it to be null when not needed

    class Config:
        from_attributes = True  # ✅ Fixed for Pydantic v2
    
#class ProviderSchema(BaseModel):
  #  id: Optional[int] = None  
   # name: str
   # email: Optional[EmailStr] = None  
    #specialty: Optional[str] = None
    #patients: List[PatientSchema] = Field(default_factory=list)  # ✅ Fixed list issue


 
