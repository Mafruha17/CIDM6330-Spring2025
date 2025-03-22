from .base_repository import BaseRepository
from mainapp.models import Provider


class ProviderRepository(BaseRepository):
    @classmethod
    def get_model(cls):
        return Provider
