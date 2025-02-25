from fastapi import FastAPI
from routers import patient_routes
from utilsclasses.custom_logger import log_info

app = FastAPI()

app.include_router(patient_routes.router)

@app.get("/")
def home():
    log_info("Home endpoint was accessed.")
    return {"message": "Welcome to the FastAPI App with SQLite!"}
