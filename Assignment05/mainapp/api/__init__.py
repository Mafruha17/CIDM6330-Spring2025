from ninja import NinjaAPI

api = NinjaAPI()

# Lazy router registration to avoid circular imports
def register_routers():
    from .api_patient import router as patient_router
    from .api_provider import router as provider_router
    from .api_device import router as device_router

    api.add_router("/patients/", patient_router)
    api.add_router("/providers/", provider_router)
    api.add_router("/devices/", device_router)

register_routers()
