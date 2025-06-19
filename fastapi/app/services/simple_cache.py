from typing import Any, Dict
import time

class SimpleCache:
    def __init__(self, ttl_seconds: int = 600):
        self.ttl = ttl_seconds
        self._store: Dict[str, Dict[str, Any]] = {}

    def __len__(self):
        return len(self.as_dict())

    def __repr__(self):
        return f"<SimpleCache ttl={self.ttl}s, size={len(self)}>"

    def __contains__(self, key: str) -> bool:
        return self.get(key) is not None

    def get(self, key: str) -> Any:
        entry = self._store.get(key)
        if not entry:
            return None

        if time.time() - entry["timestamp"] > self.ttl:
            del self._store[key]
            return None

        return entry["value"]

    def set(self, key: str, value: Any) -> None:
        self._store[key] = {
            "value": value,
            "timestamp": time.time()
        }

    def clear(self, key: str = None) -> None:
        if key:
            self._store.pop(key, None)
        else:
            self._store.clear()

    def as_dict(self) -> Dict[str, Any]:
        now = time.time()
        expired_keys = []

        result = {}
        for k, v in self._store.items():
            if now - v["timestamp"] <= self.ttl:
                result[k] = v["value"]
            else:
                expired_keys.append(k)

        for k in expired_keys:
            del self._store[k]

        return result
