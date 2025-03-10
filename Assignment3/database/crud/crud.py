from sqlmodel import Session
from database.models import Patient, Device, Provider
from schemas.patient import PatientSchema
from schemas.device import DeviceSchema
from schemas.provider import ProviderSchema
from repositories.patient_repository import PatientRepository
from repositories.device_repository import DeviceRepository
from repositories.provider_repository import ProviderRepository
from typing import Optional, List

# FIXED: Correct import of remove_device_from_patient from device_crud
from database.crud.patient_crud import (
    create_patient, get_patient, update_patient, delete_patient, 
    assign_provider_to_patient, remove_provider_from_patient as remove_provider_from_pat
)

from database.crud.device_crud import (
    create_device, get_device, update_device, delete_device,
    assign_device_to_patient, remove_device_from_patient
)

from database.crud.provider_crud import (
    create_provider, get_provider, update_provider, delete_provider,
    get_patients_by_provider
)

# NOTE: This file references your CRUD and Repositories. 
#       If you have additional bridging logic, you can add it here.
