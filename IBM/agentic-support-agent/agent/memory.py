"""
Simple long-term memory for the agent.

This models the report's "Memory" concept: preferences that should persist
across turns/sessions (e.g. "I prefer budget hotels"), as distinct from
short-lived per-conversation `state` (see state.py).

Backed by a JSON file so it survives process restarts. Swap for a real
database/table in production.
"""

import json
import os
import threading

_LOCK = threading.Lock()


class Memory:
    def __init__(self, path: str = "data/memory.json"):
        self.path = path
        self._data = self._load()

    def _load(self) -> dict:
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save(self):
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)

    def get(self, user_id: str) -> dict:
        return self._data.get(user_id, {})

    def set_preference(self, user_id: str, key: str, value):
        with _LOCK:
            self._data.setdefault(user_id, {})[key] = value
            self._save()

    def all_preferences(self, user_id: str) -> dict:
        return dict(self._data.get(user_id, {}))
