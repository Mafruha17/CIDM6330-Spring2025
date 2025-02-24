from fastapi import FastAPI
from routes.device_routes import router as device_router
from routes.healthcare_provider_routes import router as healthcare_provider_router
from routes.patient_routes import router as patient_router

app = FastAPI()

# Include routers with a prefix
app.include_router(device_router, prefix="/api")
app.include_router(healthcare_provider_router, prefix="/api")
app.include_router(patient_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "FastAPI is working!"}
