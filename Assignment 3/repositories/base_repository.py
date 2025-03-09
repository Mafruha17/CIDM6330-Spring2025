from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional
from sqlmodel import Session

T = TypeVar("T")
S = TypeVar("S")

class BaseRepository(ABC, Generic[T, S]):
    """Base repository class to be inherited by specific repositories."""

    def __init__(self, db: Session, model: T):
        self.db = db
        self.model = model

    @abstractmethod
    def create(self, data: S) -> T:
        """Create a new record."""
        pass

    @abstractmethod
    def get(self, item_id: int) -> Optional[T]:
        """Get a record by ID."""
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        """Get all records."""
        pass

    @abstractmethod
    def update(self, item_id: int, data: S) -> Optional[T]:
        """Update a record."""
        pass

    @abstractmethod
    def delete(self, item_id: int) -> bool:
        """Delete a record."""
        pass
