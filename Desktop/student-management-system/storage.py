import json
import os
from typing import List, Dict

class DataStorage:
    """Handles JSON file read/write operations with Exception Handling."""
    def __init__(self, filepath: str = "data/students.json"):
        self.filepath = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Ensures storage directory and file exist."""
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w") as file:
                json.dump([], file)

    def load_students(self) -> List[Dict]:
        """Loads records from the JSON file."""
        try:
            with open(self.filepath, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading file: {e}")
            return []

    def save_students(self, data: List[Dict]) -> bool:
        """Saves student list to the JSON file."""
        try:
            with open(self.filepath, "w") as file:
                json.dump(data, file, indent=4)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False