from fastapi import FastAPI
from routes.patient_routes import router as patient_router
from routes.healthcare_provider_routes import router as healthcare_provider_router
from routes.device_routes import router as device_router

# Create FastAPI instance
app = FastAPI(
    title="Healthcare API",
    description="An API for managing patients, providers, and devices",
    version="1.0.0"
)

# Include API routes
app.include_router(patient_router, prefix="/api", tags=["Patients"])
app.include_router(healthcare_provider_router, prefix="/api", tags=["Healthcare Providers"])
app.include_router(device_router, prefix="/api", tags=["Devices"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "FastAPI is working!"}
