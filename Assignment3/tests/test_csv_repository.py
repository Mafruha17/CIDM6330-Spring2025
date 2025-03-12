import csv
import os
from typing import List, Optional, Dict

class CSVRepository:
    """
    A repository that stores items in a CSV file (keyed by ID).
    Not fully generic: it assumes certain columns (id, name, email).
    Modify `fieldnames` to fit your use case.
    """

    def __init__(self, file_path: str):
        """
        :param file_path: Path to the CSV file used for storage.
        """
        self.file_path = file_path
        self.fieldnames = ["id", "name", "email"]  # Define expected fields

        if not os.path.exists(self.file_path):
            with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()

    def _read_csv(self) -> List[Dict[str, str]]:
        """Reads all rows from the CSV file."""
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            return list(csv.DictReader(file))

    def _write_csv(self, data: List[Dict[str, str]]):
        """Writes data to the CSV file."""
        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(data)

    def create(self, data: Dict[str, str]) -> Dict[str, str]:
        """Creates a new record in the CSV file."""
        items = self._read_csv()
        new_id = len(items) + 1  # Auto-increment ID
        data_dict = data if isinstance(data, dict) else data.model_dump()
        data_dict["id"] = str(new_id)  # Convert ID to string (CSV stores text)
        items.append(data_dict)
        self._write_csv(items)
        return data_dict

    def get(self, item_id: int) -> Optional[Dict[str, str]]:
        """Fetches a record by ID."""
        items = self._read_csv()
        return next((item for item in items if int(item["id"]) == item_id), None)

    def get_all(self) -> List[Dict[str, str]]:
        """Returns all records."""
        return self._read_csv()

    def update(self, item_id: int, data: Dict[str, str]) -> Optional[Dict[str, str]]:
        """Updates a record by ID."""
        items = self._read_csv()
        for item in items:
            if int(item["id"]) == item_id:
                update_dict = data if isinstance(data, dict) else data.model_dump(exclude_unset=True)
                for key, value in update_dict.items():
                    if key in item:
                        item[key] = value  # Update only known fields
                self._write_csv(items)
                return item
        return None

    def delete(self, item_id: int) -> bool:
        """Deletes a record by ID."""
        items = self._read_csv()
        remaining = [item for item in items if int(item["id"]) != item_id]
        if len(remaining) != len(items):
            self._write_csv(remaining)
            return True
        return False
