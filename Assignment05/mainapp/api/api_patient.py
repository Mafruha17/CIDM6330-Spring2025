# mainapp/api/api_patient.py

from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404
from mainapp.models import Patient
from mainapp.schemas.patient_schema import PatientIn, PatientOut

router = Router()

@router.get("/", response=List[PatientOut])
def list_patients(request):
    patients = Patient.objects.prefetch_related("devices", "providers").all()
    return patients

@router.get("/{patient_id}", response=PatientOut)
def get_patient(request, patient_id: int):
    return get_object_or_404(Patient.objects.prefetch_related("devices", "providers"), id=patient_id)

@router.post("/", response=PatientOut)
def create_patient(request, data: PatientIn):
    return Patient.objects.create(**data.dict())

@router.put("/{patient_id}", response=PatientOut)
def update_patient(request, patient_id: int, data: PatientIn):
    patient = get_object_or_404(Patient, id=patient_id)
    for field, value in data.dict().items():
        setattr(patient, field, value)
    patient.save()
    return patient

@router.delete("/{patient_id}")
def delete_patient(request, patient_id: int):
    patient = get_object_or_404(Patient, id=patient_id)
    patient.delete()
    return {"message": "Patient deleted"}
