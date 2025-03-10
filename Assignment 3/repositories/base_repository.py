from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional
from sqlmodel import Session, select

T = TypeVar("T")
S = TypeVar("S")

class BaseRepository(ABC, Generic[T, S]):
    """Base repository class to be inherited by specific repositories."""

    def __init__(self, db: Session, model: T):
        self.db = db
        self.model = model

    @abstractmethod
    def create(self, data: S) -> T:
        pass

    def get(self, item_id: int) -> Optional[T]:
        statement = select(self.model).where(self.model.id == item_id)
        return self.db.exec(statement).first()

    def get_all(self) -> List[T]:
        statement = select(self.model)
        return self.db.exec(statement).all()

    @abstractmethod
    def update(self, item_id: int, data: S) -> Optional[T]:
        pass

    def delete(self, item_id: int) -> bool:
        statement = select(self.model).where(self.model.id == item_id)
        obj = self.db.exec(statement).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False
