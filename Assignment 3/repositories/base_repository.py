from abc import ABC, abstractmethod
from typing import List, Optional

class BaseRepository(ABC):
    """Abstract base class for all repositories."""

    @abstractmethod
    def create(self, data):
        pass

    @abstractmethod
    def get(self, item_id: int):
        pass

    @abstractmethod
    def get_all(self) -> List:
        pass

    @abstractmethod
    def update(self, item_id: int, data):
        pass

    @abstractmethod
    def delete(self, item_id: int):
        pass
