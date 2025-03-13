from pydantic import BaseModel # ConfigDict
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
     orm_mode = True  # Enables serialization from ORM models


   # model_config = ConfigDict(from_attributes=True)  # ✅ New Pydantic V2 style
