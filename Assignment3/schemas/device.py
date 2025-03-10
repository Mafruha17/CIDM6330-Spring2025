from pydantic import BaseModel, ConfigDict
from typing import Optional

class DeviceSchema(BaseModel):
    """
    A Pydantic schema for Devices, with `from_attributes=True`
    so we can directly return SQLModel objects in FastAPI responses.
    """
    id: int
    serial_number: str
    patient_id: Optional[int] = None
    active: bool = True

    model_config = ConfigDict(from_attributes=True)
