# Assignment05/ai_services/api_ai.py

from ninja import Router
from pydantic import BaseModel

from .services import summarize_note, detect_device_anomaly

router = Router(tags=["AI Services"])

class NoteIn(BaseModel):
    text: str
    language: str = "en"

@router.post("/summaries")
def create_summary(request, data: NoteIn):
    summary = summarize_note(data.text, data.language)
    return {"summary": summary}

class DeviceDataIn(BaseModel):
    readings: list[float]

@router.post("/device-anomalies")
def check_anomaly(request, data: DeviceDataIn):
    result = detect_device_anomaly(data.readings)
    return {"anomaly": result}
