"""Bounded threadpool execution; failures remain associated with devices."""
from concurrent.futures import ThreadPoolExecutor, as_completed

def run_fleet(devices, worker, max_workers=12):
    if not (1 <= max_workers <= 32):
        raise ValueError("max_workers must be between 1 and 32")
    unique = [dict(d) for d in devices]
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        tasks = {pool.submit(worker, device): device["name"] for device in unique}
        for future in as_completed(tasks):
            name = tasks[future]
            try:
                results[name] = {"ok": True, "data": future.result()}
            except Exception as exc:
                results[name] = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
    return dict(sorted(results.items()))

