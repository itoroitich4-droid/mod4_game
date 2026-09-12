import json
import os

class DataStorage:
    @staticmethod
    def load_json(filepath: str) -> dict:
        if not os.path.exists(filepath):
            return {}
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    @staticmethod
    def save_json(filepath: str, data: dict) -> bool:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except IOError:
            return False