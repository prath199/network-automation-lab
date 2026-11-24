from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python"))
from netops.fleet import run_fleet

def test_scale_and_order():
    devices = [{"name": f"node-{i:04d}"} for i in range(300)]
    results = run_fleet(devices, lambda device: device["name"], max_workers=12)
    assert list(results) == sorted(results)
    assert len(results) == 300
    assert all(result["ok"] for result in results.values())

def test_error_isolated():
    nodes = [{"name":"ok"},{"name":"fail"}]
    def operation(node):
        if node["name"] == "fail":
            raise ValueError("offline")
        return 1
    results = run_fleet(nodes, operation, max_workers=2)
    assert results["ok"]["ok"] and not results["fail"]["ok"]

