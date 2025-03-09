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
class CSVRepository(BaseRepository):
    """Implements repository using CSV storage."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.fieldnames = ["id", "name", "email"]

        if not os.path.exists(self.file_path):
            with open(self.file_path, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()

    def _read_csv(self) -> List[dict]:
        with open(self.file_path, mode='r', newline='') as file:
            return list(csv.DictReader(file))

    def _write_csv(self, data: List[dict]):
        with open(self.file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(data)

    def create(self, data: ProviderSchema):
        items = self._read_csv()
        data_dict = data.model_dump()
        data_dict["id"] = len(items) + 1
        items.append(data_dict)
        self._write_csv(items)
        return data_dict

    def get(self, item_id: int):
        items = self._read_csv()
        return next((item for item in items if int(item["id"]) == item_id), None)

    def get_all(self):
        return self._read_csv()

    def update(self, item_id: int, data: ProviderSchema):
        items = self._read_csv()
        for item in items:
            if int(item["id"]) == item_id:
                item.update(data.model_dump(exclude_unset=True))
                self._write_csv(items)
                return item
        return None

    def delete(self, item_id: int):
        items = self._read_csv()
        new_items = [item for item in items if int(item["id"]) != item_id]
        if len(new_items) == len(items):
            return False
        self._write_csv(new_items)
        return True