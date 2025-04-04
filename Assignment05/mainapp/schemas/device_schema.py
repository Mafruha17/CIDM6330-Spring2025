from __future__ import annotations
from ninja import Schema
from typing import Optional
from pydantic import field_validator

class DeviceIn(Schema):
    serial_number: str
    patient_id: Optional[int] = None
    active: bool = True

    @field_validator("patient_id", mode="before")
    def convert_zero_to_none(cls, value):
        if value == 0:
            return None
        return value

class DeviceOut(Schema):
    id: int
    serial_number: str
    patient_id: Optional[int]
    active: bool
