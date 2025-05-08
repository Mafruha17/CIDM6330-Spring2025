from ninja import NinjaAPI

api = NinjaAPI(version="1.0.0", urls_namespace="api")  # ✅ versioning and namespacing

@api.get("/", tags=["Root"])  # ✅ this fixes the /api/ 404 issue
def api_root(request):
    return {"message": "Welcome to the API root. Try /patients/, /providers/, or /ai/summaries"}

from mainapp.api.api_patient import router as patient_router
from mainapp.api.api_provider import router as provider_router
from mainapp.api.api_device import router as device_router

# ✅ Optional AI router (commented out safely if not needed here)
# from ai_services.api_ai import router as ai_router
# api.add_router("/ai/", ai_router, tags=["AI"])

api.add_router("/patients/", patient_router, tags=["Patients"])  # ✅ routes
api.add_router("/providers/", provider_router, tags=["Providers"])
api.add_router("/devices/", device_router, tags=["Devices"])
