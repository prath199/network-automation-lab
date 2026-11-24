#!/usr/bin/env python3
import argparse
from netops.common import load_inventory, write_report
from netops.fleet import run_fleet
from netops.transport import show

def audit(device):
    commands = (["show interfaces status", "show interfaces counters errors"]
                if device["platform"] == "arista_eos" else
                ["show interfaces status", "show interfaces"])
    return {command: show(device, command) for command in commands}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inventory", required=True)
    ap.add_argument("--output", default="outputs/interfaces.json")
    ap.add_argument("--workers", type=int, default=12)
    a = ap.parse_args()
    results = run_fleet(load_inventory(a.inventory), audit, a.workers)
    write_report(a.output, results)
    if any(not r["ok"] for r in results.values()):
        raise SystemExit(2)
if __name__ == "__main__":
    main()

