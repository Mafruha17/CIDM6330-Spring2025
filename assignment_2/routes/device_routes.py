from fastapi import APIRouter

router = APIRouter()

@router.get("/devices/")
def get_devices():
    return {"message": "List of devices"}
