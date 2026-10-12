import os
import json
import tempfile
from datetime import datetime

class EngagementLedger:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._data: dict[str, dict] = {}
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except Exception:
                self._data = {}
        else:
            self._data = {}

    def has(self, comment_id: str) -> bool:
        return comment_id in self._data

    def get(self, comment_id: str) -> dict | None:
        return self._data.get(comment_id)

    def record(self, comment_id: str, author: str, actions: list[str], reply_text: str = "", status: str = "success") -> None:
        self._data[comment_id] = {
            "timestamp": datetime.now().isoformat(),
            "author": author,
            "actions": actions,
            "reply_text": reply_text,
            "status": status,
        }

    def save(self) -> None:
        os.makedirs(os.path.dirname(os.path.abspath(self.file_path)), exist_ok=True)
        # Atomic write via tempfile
        dir_name = os.path.dirname(os.path.abspath(self.file_path))
        with tempfile.NamedTemporaryFile("w", dir=dir_name, delete=False, encoding="utf-8") as tf:
            json.dump(self._data, tf, ensure_ascii=False, indent=2)
            temp_name = tf.name
        os.replace(temp_name, self.file_path)
