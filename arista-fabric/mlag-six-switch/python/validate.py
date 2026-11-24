#!/usr/bin/env python3
"""Use case 01: validate MLAG inventory before any rendering or deployment."""
from model import load, validate
if __name__ == "__main__":
    data = load()
    validate(data)
    print(f"Source of truth OK: {len(data['devices'])} devices in {len(data['pairs'])} MLAG pairs")
