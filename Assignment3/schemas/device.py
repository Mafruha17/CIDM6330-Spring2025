from pydantic import BaseModel
from typing import Optional

class DeviceSchema(BaseModel):
    """
    A Pydantic schema for Devices.
    Using `orm_mode=True` to allow SQLModel objects to be serialized in FastAPI responses.
    """
    id: Optional[int] = None  # Make id optional
    serial_number: str
    patient_id: Optional[int] = None
    active: bool = True

    
    class Config:
        from_attributes = True  # ✅ Update for Pydantic V2
