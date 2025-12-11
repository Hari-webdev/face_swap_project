import json
import os
import threading
from typing import Dict, Any

STORE_FILE = "app/job_store_data.json"
_lock = threading.Lock()


class JobStore:
    def __init__(self):
        self._data: Dict[str, Any] = {}
        self._load()
    
    def _load(self):
        """Load jobs from file"""
        if os.path.exists(STORE_FILE):
            try:
                with open(STORE_FILE, 'r') as f:
                    self._data = json.load(f)
            except:
                self._data = {}
    
    def _save(self):
        """Save jobs to file"""
        try:
            with open(STORE_FILE, 'w') as f:
                json.dump(self._data, f, default=str, indent=2)
        except Exception as e:
            print(f"Error saving job store: {e}")
    
    def __getitem__(self, key: str) -> Dict[str, Any]:
        with _lock:
            return self._data[key]
    
    def __setitem__(self, key: str, value: Dict[str, Any]):
        with _lock:
            self._data[key] = value
            self._save()
    
    def __contains__(self, key: str) -> bool:
        with _lock:
            return key in self._data
    
    def get(self, key: str, default=None):
        with _lock:
            return self._data.get(key, default)
    
    def keys(self):
        with _lock:
            return self._data.keys()
    
    def values(self):
        with _lock:
            return self._data.values()
    
    def items(self):
        with _lock:
            return self._data.items()


job_store = JobStore()
