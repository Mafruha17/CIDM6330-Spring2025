from pydantic import BaseModel, ConfigDict
from typing import Optional

class DeviceSchema(BaseModel):
    id: int
    serial_number: str
    patient_id: Optional[int] = None
    active: bool = True

    model_config = ConfigDict(from_attributes=True)