#!/usr/bin/env python3
"""Read-only PAN-OS software and HA discovery for an approved change review."""
import argparse
import json
import os
import xml.etree.ElementTree as ET
import requests

def op(host, key, command, ca_bundle):
    response = requests.get(f"https://{host}/api/", params={
        "type": "op", "cmd": command, "key": key
    }, verify=ca_bundle, timeout=(5, 45), allow_redirects=False)
    response.raise_for_status()
    root = ET.fromstring(response.content)
    if root.attrib.get("status") != "success":
        raise RuntimeError(f"PAN-OS operational request failed: {root.attrib.get('status')}")
    return ET.tostring(root.find("result"), encoding="unicode") if root.find("result") is not None else ""

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--host", required=True)
    p.add_argument("--api-key-env", required=True)
    p.add_argument("--target-version", required=True)
    p.add_argument("--ca-bundle", required=True)
    args = p.parse_args()
    key = os.environ[args.api_key_env]
    system = op(args.host, key, "<show><system><info/></system></show>",args.ca_bundle)
    ha = op(args.host, key, "<show><high-availability><state/></high-availability></show>",args.ca_bundle)
    print(json.dumps({"host": args.host, "target_version": args.target_version,
                      "upgrade_executed": False, "system": system, "ha": ha}, indent=2))
    print("MANUAL GATE: confirm release path, backup, HA readiness, vendor prerequisites and rollback.")
if __name__ == "__main__":
    main()

