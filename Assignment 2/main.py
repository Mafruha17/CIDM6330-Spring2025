from fastapi import FastAPI
from routers import patient_routes

app = FastAPI()

app.include_router(patient_routes.router)

@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI App with SQLite!"}
