#!/usr/bin/env python3
"""Export running PAN-OS config from allowlisted firewalls, without changes."""
import argparse
import os
from pathlib import Path
import tempfile
import xml.etree.ElementTree as ET
import requests
import yaml

def backup(device, out, ca_bundle):
    token = os.environ[device["api_key_env"]]
    host = device["host"]
    r = requests.get(f"https://{host}/api/", params={"type": "export", "category": "configuration",
                   "key": token}, verify=ca_bundle, timeout=(5, 60), allow_redirects=False)
    r.raise_for_status()
    if not r.content:
        raise RuntimeError(f"No export data from {device['name']}")
    root = ET.fromstring(r.content)
    if root.tag == "response" and root.attrib.get("status") == "error":
        raise RuntimeError("PAN-OS export returned API error")
    output = Path(out); output.mkdir(parents=True, exist_ok=True)
    target = output / (device["name"] + ".xml")
    with tempfile.NamedTemporaryFile(mode="wb", dir=output, delete=False) as handle:
        os.chmod(handle.name, 0o600)
        handle.write(r.content)
        temp = handle.name
    Path(temp).replace(target)
    return str(target)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--inventory", required=True)
    p.add_argument("--output", default="outputs/panos")
    p.add_argument("--ca-bundle", required=True)
    args = p.parse_args()
    devices = yaml.safe_load(Path(args.inventory).read_text())["devices"]
    for device in devices:
        backup(device,args.output,args.ca_bundle)
if __name__ == "__main__":
    main()

