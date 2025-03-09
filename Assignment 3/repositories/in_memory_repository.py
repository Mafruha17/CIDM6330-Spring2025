from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database.connection import get_db
from database.crud.crud import (
    create_provider, get_provider, update_provider, delete_provider
)
from schemas.provider import ProviderSchema
import csv
import os
from typing import List, Dict, Optional
from repositories.base_repository import BaseRepository

router = APIRouter(prefix="/providers", tags=["Providers"])

# ✅ In-Memory Repository
class InMemoryRepository(BaseRepository):
    """Implements repository using an in-memory Python dictionary."""
    
    def __init__(self):
        self.data: Dict[int, ProviderSchema] = {}
        self.current_id = 1

    def create(self, data: ProviderSchema) -> ProviderSchema:
        data_dict = data.model_dump()
        data_dict["id"] = self.current_id
        self.data[self.current_id] = data_dict
        self.current_id += 1
        return data_dict

    def get(self, item_id: int):
        return self.data.get(item_id)

    def get_all(self) -> List[Dict]:
        return list(self.data.values())

    def update(self, item_id: int, data: ProviderSchema):
        if item_id in self.data:
            self.data[item_id].update(data.model_dump(exclude_unset=True))
            return self.data[item_id]
        return None

    def delete(self, item_id: int) -> bool:
        return self.data.pop(item_id, None) is not None