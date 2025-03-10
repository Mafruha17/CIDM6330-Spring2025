from fastapi import FastAPI
from database.connection import get_db
from routers import patient_routes, device_routes, provider_routes

app = FastAPI(
    title="Healthcare API",
    description="A FastAPI application for managing Patients, Devices, and Providers",
    version="1.0.0"
)

# ✅ Include the routers
app.include_router(patient_routes.router)
app.include_router(device_routes.router)
app.include_router(provider_routes.router)

@app.get("/")
def root():
    return {"message": "API is running"}
