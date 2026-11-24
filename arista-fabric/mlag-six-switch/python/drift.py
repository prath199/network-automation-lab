#!/usr/bin/env python3
"""Use case 10: offline read-only drift comparison with captured show running-config."""
import argparse
import difflib
import json
import re
from pathlib import Path
from model import ROOT

IGNORE = re.compile(r"^(!|\s*$|!.*last modified)", re.I)
def normalize(text):
    return [line.rstrip() for line in text.splitlines() if not IGNORE.match(line)]

def compare(expected, observed):
    return list(difflib.unified_diff(normalize(expected), normalize(observed),
                                    fromfile="approved",tofile="captured",lineterm=""))

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--approved", required=True, help="approved configuration directory")
    p.add_argument("--captured", required=True, help="read-only backup directory")
    p.add_argument("--output",default=str(ROOT/"reports/drift.json"))
    args = p.parse_args()
    results = {}
    for expected in sorted(Path(args.approved).glob("*.cfg")):
        actual = Path(args.captured)/expected.name
        if actual.exists():
            diff = compare(expected.read_text(), actual.read_text())
            results[expected.stem] = {"drift": bool(diff), "diff": diff}
        else:
            results[expected.stem] = {"error": "Capture missing"}
    target=Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(results,indent=2)+"\n")
    print(f"Wrote report: {target}")
    if any(row.get("drift") or row.get("error") for row in results.values()):
        raise SystemExit(2)
if __name__ == "__main__":
    main()
