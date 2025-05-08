from ninja import Schema

class SummaryRequest(Schema):
    text: str

class SummaryResponse(Schema):
    summary: str

class DeviceAnomalyRequest(Schema):
    serial_number: str
    status_data: str  # e.g. JSON string or encoded status info

class DeviceAnomalyResponse(Schema):
    is_anomalous: bool
    details: str
