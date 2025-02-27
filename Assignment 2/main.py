from fastapi import FastAPI
from utilsclasses.custom_logger import log_info
from routers import patient_routes, device_routes, provider_routes  # Import both routers
#from .routers import patient_routes, device_routes


log_info("Starting FastAPI application...")
app = FastAPI()

# Include both patient and device routers
app.include_router(patient_routes.router)
app.include_router(device_routes.router)
app.include_router(provider_routes.router)

@app.get("/")
def home():
    log_info("Home endpoint was accessed.")
    return {"message": "Welcome to the FastAPI App with SQLite!"}
