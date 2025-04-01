from ninja import NinjaAPI, Schema
from typing import List
from django.shortcuts import get_object_or_404
from mainapp.models import Patient, Device, Provider

api = NinjaAPI()

@api.get("/patients/", response=List[PatientOutSchema])
def list_patients(request):
    return Patient.objects.all()

@api.post("/patients/", response=PatientOutSchema)
def create_patient(request, data: PatientSchema):
    patient = Patient.objects.create(**data.dict())
    return patient

@api.get("/patients/{patient_id}/", response=PatientOutSchema)
def get_patient(request, patient_id: int):
    patient = get_object_or_404(Patient, id=patient_id)
    return patient