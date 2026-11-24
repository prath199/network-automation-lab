#!/usr/bin/env python3
import argparse
import difflib
from pathlib import Path
from netops.common import load_inventory, write_report
from netops.fleet import run_fleet
from netops.transport import show

def collect(device, directory):
    baseline = Path(directory, device["name"] + ".cfg")
    if not baseline.is_file():
        raise FileNotFoundError(f"Missing approved baseline for {device['name']}")
    before = baseline.read_text(encoding="utf-8").splitlines()
    live = show(device, "show running-config").splitlines()
    diff = list(difflib.unified_diff(before, live, fromfile="approved", tofile="live", lineterm=""))
    return {"drift": bool(diff), "diff": diff}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inventory", required=True)
    ap.add_argument("--baselines", required=True)
    ap.add_argument("--output", default="outputs/drift.json")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()
    outcome = run_fleet(load_inventory(args.inventory), lambda d: collect(d,args.baselines), args.workers)
    write_report(args.output, outcome)
    if any(not r["ok"] or r["data"]["drift"] for r in outcome.values()):
        raise SystemExit(2)
if __name__ == "__main__":
    main()

