# ✅ Configure logging to terminal only (Remove File Logging)
import logging
import traceback
from fastapi import FastAPI, Request
from database.connection import get_db
from routers import patient_routes, device_routes, provider_routes
from fastapi.responses import JSONResponse

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # ✅ Only print logs to the terminal
    ]
)

app = FastAPI(
    title="Healthcare API",
    description="A FastAPI application for managing Patients, Devices, and Providers",
    version="1.0.0"
)

# ✅ Global error handler - Print full traceback to the terminal
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print("\n" + "=" * 50)
    print(f"🔥 ERROR in {request.url}: {str(exc)}")
    traceback.print_exc()
    print("=" * 50 + "\n")

    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal Server Error: {str(exc)}"},  # ✅ Show real error
    )

# Include both patient and device routers
app.include_router(patient_routes.router)
app.include_router(device_routes.router)
app.include_router(provider_routes.router)

@app.get("/")
def root():
    return {"message": "API is running"}
