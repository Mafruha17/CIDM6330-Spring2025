from .base_repository import BaseRepository
from mainapp.models import Device


class DeviceRepository(BaseRepository):
    @classmethod
    def get_model(cls):
        return Device

    @classmethod
    def get_unassigned_devices(cls):
        return cls.get_model().objects.filter(patient__isnull=True)
