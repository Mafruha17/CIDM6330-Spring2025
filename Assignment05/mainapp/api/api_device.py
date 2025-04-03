# ✅ API Modules: Device Endpoints Using Django Ninja

# mainapp/api/api_device.py
from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404
from mainapp.models import Device
from mainapp.schemas.device_schema import DeviceIn, DeviceOut

router = Router()

@router.get("/", response=List[DeviceOut])
def list_devices(request):
    return Device.objects.all()

@router.get("/{device_id}", response=DeviceOut)
def get_device(request, device_id: int):
    return get_object_or_404(Device, id=device_id)

@router.post("/", response=DeviceOut)
def create_device(request, data: DeviceIn):
    return Device.objects.create(**data.dict())

@router.put("/{device_id}", response=DeviceOut)
def update_device(request, device_id: int, data: DeviceIn):
    device = get_object_or_404(Device, id=device_id)
    for field, value in data.dict().items():
        setattr(device, field, value)
    device.save()
    return device

@router.delete("/{device_id}")
def delete_device(request, device_id: int):
    device = get_object_or_404(Device, id=device_id)
    device.delete()
    return {"message": "Device deleted"}
