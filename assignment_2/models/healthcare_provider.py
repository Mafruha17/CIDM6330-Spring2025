from pydantic import BaseModel

class HealthcareProvider(BaseModel):
    id: int
    name: str
    specialty: str
