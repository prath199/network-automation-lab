"""Inventory and result management utilities for bounded fleet automation."""
import json
import os
from pathlib import Path
import yaml

ALLOWED = {"cisco_ios", "arista_eos"}
def load_inventory(path):
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    devices = data.get("devices", []) if isinstance(data, dict) else []
    names = [d["name"] for d in devices]
    if len(names) != len(set(names)):
        raise ValueError("Duplicate device names")
    for d in devices:
        if d.get("platform") not in ALLOWED:
            raise ValueError(f"Unsupported platform for {d.get('name')}")
        if not d.get("host") or not d.get("credential_env"):
            raise ValueError("Missing host or credential_env")
    return devices

def auth_env(device):
    key = device["credential_env"]
    password = os.getenv(key)
    if not password:
        raise RuntimeError(f"Missing credential environment variable: {key}")
    return password

def write_report(path, data):
    file = Path(path)
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return str(file)

