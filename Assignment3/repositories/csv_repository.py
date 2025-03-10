import csv
import os
from typing import List, Optional, Dict
from repositories.base_repository import BaseRepository

# In a CSV approach, we typically *don't* need a Session or Model, so it can be ignored.

class CSVRepository(BaseRepository):
    """
    Example repository storing items in a CSV file (keyed by ID).
    Not fully generic: it assumes certain columns (id, name, email).
    Modify fieldnames to fit your use case.
    """

    def __init__(self, file_path: str):
        """
        :param file_path: Path to the CSV file used for storage.
        """
        # We won't call super().__init__ because we don't need a db session or model.
        self.file_path = file_path
        self.fieldnames = ["id", "name", "email"]

        if not os.path.exists(self.file_path):
            with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()

    def _read_csv(self) -> List[dict]:
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            return list(csv.DictReader(file))

    def _write_csv(self, data: List[dict]):
        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(data)

    def create(self, data):
        items = self._read_csv()

        # Expecting 'data' to be a Pydantic/SQLModel that has .model_dump() or a dict
        data_dict = data.model_dump() if hasattr(data, "model_dump") else dict(data)
        data_dict["id"] = len(items) + 1  # Simple auto-increment
        items.append(data_dict)
        self._write_csv(items)
        return data_dict

    def get(self, item_id: int):
        # Overriding get() from BaseRepository, ignoring SQL
        items = self._read_csv()
        return next((item for item in items if int(item["id"]) == item_id), None)

    def get_all(self):
        # Overriding get_all() from BaseRepository
        return self._read_csv()

    def update(self, item_id: int, data) -> Optional[dict]:
        items = self._read_csv()
        for item in items:
            if int(item["id"]) == item_id:
                update_dict = data.model_dump(exclude_unset=True) if hasattr(data, "model_dump") else dict(data)
                for key, value in update_dict.items():
                    # Only update known fields
                    if key in item:
                        item[key] = value
                self._write_csv(items)
                return item
        return None

    def delete(self, item_id: int) -> bool:
        items = self._read_csv()
        remaining = [item for item in items if int(item["id"]) != item_id]
        if len(remaining) != len(items):
            self._write_csv(remaining)
            return True
        return False
