import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TOKENS_FILE = BASE_DIR / "tokens.json"
CONFIG_FILE = BASE_DIR / "config.json"

def load_tokens():
    if not TOKENS_FILE.exists():
        return {}
    try:
        with open(TOKENS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_tokens(data):
    with open(TOKENS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
            if config.get("admin_user") and config.get("admin_pass"):
                return config
        except (OSError, json.JSONDecodeError):
            pass

    env_user = os.environ.get("ADMIN_USER")
    env_pass = os.environ.get("ADMIN_PASS")
    if env_user and env_pass:
        return {"admin_user": env_user, "admin_pass": env_pass}
    if os.environ.get("RAILWAY_ENVIRONMENT"):
        raise RuntimeError("ADMIN_USER and ADMIN_PASS must be configured in Railway")

    default_config = {
        "admin_user": "admin",
        "admin_pass": "admin123"
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(default_config, f, indent=4)
    return default_config
