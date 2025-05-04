from ninja import NinjaAPI

api = NinjaAPI(version="1.0.0", urls_namespace="api")

from mainapp.api.api_patient import router as patient_router
from mainapp.api.api_provider import router as provider_router
from mainapp.api.api_device import router as device_router

#from ai_services.api_ai import router as ai_router
#api.add_router("/ai/", ai_router, tags=["AI"])

api.add_router("/patients/", patient_router, tags=["Patients"])
api.add_router("/providers/", provider_router, tags=["Providers"])
api.add_router("/devices/", device_router, tags=["Devices"])
