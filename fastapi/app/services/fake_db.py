from pathlib import Path
import json

FILE = Path("users.json")

def load_users():
    if FILE.exists():
        return json.loads(FILE.read_text())
    return {}

def save_users(data):
    FILE.write_text(json.dumps(data, indent=2))

# Fake in-memory "database"
fake_users_db = load_users()