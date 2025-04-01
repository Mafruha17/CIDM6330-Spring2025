from .base_repository import BaseRepository
from mainapp.models import Patient


class PatientRepository(BaseRepository):
    @classmethod
    def get_model(cls):
        return Patient

    @classmethod
    def get_active_patients(cls):
        return cls.get_model().objects.filter(active=True)
