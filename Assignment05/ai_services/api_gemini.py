from ninja import Router
from .schemas import SummaryRequest, SummaryResponse, DeviceAnomalyRequest, DeviceAnomalyResponse
from .gemini_services import summarize_text, detect_device_anomaly

ai_router = Router(tags=["AI Services"])

@ai_router.post("/summaries", response=SummaryResponse)
def get_summary(request, payload: SummaryRequest):
    return summarize_text(payload)

@ai_router.post("/tests", response=DeviceAnomalyResponse)
def test_anomaly(request, payload: DeviceAnomalyRequest):
    return detect_device_anomaly(payload)
