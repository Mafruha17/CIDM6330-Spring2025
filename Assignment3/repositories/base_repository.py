from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional
from sqlmodel import Session, select

T = TypeVar("T")  # The ORM model type (e.g., Patient, Provider, etc.)
S = TypeVar("S")  # The Pydantic/SQLModel schema type

class BaseRepository(ABC, Generic[T, S]):
    """
    Base repository class to be inherited by specific repositories.
    Provides default CRUD-like methods (get, get_all, delete),
    while create/update remain abstract if you need specialized logic.
    """

    def __init__(self, db: Session, model: T):
        """
        :param db: The database session (if using SQL-based storage)
        :param model: The SQLModel/ORM model class
        """
        self.db = db
        self.model = model

    @abstractmethod
    def create(self, data: S) -> T:
        """
        Creates a new record in the underlying storage.
        Must be implemented by subclasses.
        """
        pass

    def get(self, item_id: int) -> Optional[T]:
        """
        Retrieves a single record by ID using a SQL query (if using SQL).
        Subclasses can override as needed.
        """
        statement = select(self.model).where(self.model.id == item_id)
        return self.db.exec(statement).first()

    def get_all(self) -> List[T]:
        """
        Retrieves all records of this model.
        Subclasses can override to implement alternative storage.
        """
        statement = select(self.model)
        return self.db.exec(statement).all()

    @abstractmethod
    def update(self, item_id: int, data: S) -> Optional[T]:
        """
        Updates an existing record.
        Must be implemented by subclasses.
        """
        pass

    def delete(self, item_id: int) -> bool:
        """
        Deletes a record by ID (SQL-based default).
        Subclasses can override for CSV or in-memory usage if needed.
        """
        statement = select(self.model).where(self.model.id == item_id)
        obj = self.db.exec(statement).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False
