from pydantic import BaseModel

class DeviceSchema(BaseModel):
    id: int
    serial_number: str
    patient_id: int | None = None

    class Config:
        from_attributes = True
