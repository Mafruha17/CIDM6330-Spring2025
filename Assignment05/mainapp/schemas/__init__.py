# mainapp/schemas/__init__.py

from .patient_schema import PatientOut
from .provider_schema import ProviderOut
from .device_schema import DeviceOut

# Rebuild all models to resolve forward references
PatientOut.model_rebuild()
ProviderOut.model_rebuild()
DeviceOut.model_rebuild()
