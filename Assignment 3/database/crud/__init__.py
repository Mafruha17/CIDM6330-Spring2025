from .patient_crud import (
    create_patient,
    get_patient,
    assign_provider_to_patient,
    remove_provider_from_patient,
    delete_patient
)

from .provider_crud import (
    create_provider,
    get_provider,
    delete_provider,
    get_patients_by_provider  # ✅ Ensure function is defined in provider_crud.py
)

from .device_crud import (
    create_device,
    get_device,
    assign_device_to_patient,
    delete_device
)
