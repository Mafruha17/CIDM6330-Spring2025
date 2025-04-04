from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404
from mainapp.models import Device, Patient
from mainapp.schemas.device_schema import DeviceIn, DeviceOut
from django.core.exceptions import ValidationError

router = Router()

@router.get("/", response=List[DeviceOut])
def list_devices(request):
    return Device.objects.all()

@router.get("/{device_id}", response=DeviceOut)
def get_device(request, device_id: int):
    return get_object_or_404(Device, id=device_id)

@router.post("/", response=DeviceOut)
def create_device(request, data: DeviceIn):
    # If a patient_id is provided, ensure that the patient exists.
    if data.patient_id is not None:
        # This will raise a 404 error if the patient doesn't exist.
        get_object_or_404(Patient, id=data.patient_id)
    return Device.objects.create(**data.dict())

@router.put("/{device_id}", response=DeviceOut)
def update_device(request, device_id: int, data: DeviceIn):
    device = get_object_or_404(Device, id=device_id)
    if data.patient_id is not None:
        get_object_or_404(Patient, id=data.patient_id)
    for field, value in data.dict().items():
        setattr(device, field, value)
    device.save()
    return device

@router.delete("/{device_id}")
def delete_device(request, device_id: int):
    device = get_object_or_404(Device, id=device_id)
    try:
        device.delete()
    except ValidationError as e:
        return {"error": str(e)}
    return {"message": "Device deleted"}

# Additional endpoints for assignment/unassignment
@router.post("/{device_id}/assign/", response=DeviceOut)
def assign_device(request, device_id: int, patient_id: int):
    device = get_object_or_404(Device, id=device_id)
    # Ensure the patient exists
    patient = get_object_or_404(Patient, id=patient_id)
    device.patient = patient
    device.save()
    return device

@router.post("/{device_id}/unassign/", response=DeviceOut)
def unassign_device(request, device_id: int):
    device = get_object_or_404(Device, id=device_id)
    device.patient = None
    device.save()
    return device
