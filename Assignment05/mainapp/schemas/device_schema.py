from ninja import Schema
from typing import Optional

class DeviceIn(Schema):
    serial_number: str
    patient_id: Optional[int] = None
    active: bool = True

class DeviceOut(DeviceIn):
    id: int
