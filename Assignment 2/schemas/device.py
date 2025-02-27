from pydantic import BaseModel
from typing import Optional

class DeviceSchema(BaseModel):
    id: int
    serial_number: str
    patient_id: Optional[int] = None  # ✅ Fix: Foreign Key
    active: bool = True

    class Config:
        from_attributes = True
