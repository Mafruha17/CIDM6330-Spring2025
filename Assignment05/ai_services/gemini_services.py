from .gemini import model
from .schemas import SummaryRequest, SummaryResponse, DeviceAnomalyRequest, DeviceAnomalyResponse

def summarize_text(request: SummaryRequest) -> SummaryResponse:
    prompt = f"Summarize this medical text:\n\n{request.text}"
    response = model.generate_content(prompt)
    return SummaryResponse(summary=response.text.strip())

def detect_device_anomaly(request: DeviceAnomalyRequest) -> DeviceAnomalyResponse:
    prompt = (
        f"Analyze the following device status data for anomalies:\n"
        f"{request.status_data}\n\n"
        "Is there any sign of malfunction or abnormal readings?"
    )
    response = model.generate_content(prompt)
    flagged = "yes" in response.text.lower()
    return DeviceAnomalyResponse(is_anomalous=flagged, details=response.text.strip())

