from typing import Dict, List, Optional
from repositories.base_repository import BaseRepository

class InMemoryRepository(BaseRepository):
    """
    Implements repository using an in-memory Python dictionary.
    Note: This example is not strongly typed with T, S because
    we are storing generic dictionaries. Adjust if needed.
    """

    def __init__(self):
        # We won't call super() because we do not have a db session or model class here.
        self.data: Dict[int, dict] = {}
        self.current_id = 1

    def create(self, obj_in) -> dict:
        """
        Expects obj_in to be a dictionary or an object with .dict().
        """
        if hasattr(obj_in, "dict"):
            item_dict = obj_in.dict()
        else:
            item_dict = dict(obj_in)

        item_dict["id"] = self.current_id
        self.data[self.current_id] = item_dict
        self.current_id += 1
        return item_dict

    def get(self, item_id: int) -> Optional[dict]:
        return self.data.get(item_id)

    def get_all(self) -> List[dict]:
        return list(self.data.values()) if self.data else []  # Ensure empty list instead of None

    def update(self, item_id: int, obj_in) -> Optional[dict]:
        """
        Updates an existing item while keeping required fields intact.
        """
        if item_id not in self.data:
            return None

        if hasattr(obj_in, "dict"):
            update_dict = obj_in.dict(exclude_unset=True)
        else:
            update_dict = dict(obj_in)

        existing_item = self.data[item_id]

        for key, value in update_dict.items():
            if value is not None:  # Prevent removing required fields
                existing_item[key] = value

        self.data[item_id] = existing_item
        return existing_item

    def delete(self, item_id: int) -> bool:
        return self.data.pop(item_id, None) is not None
