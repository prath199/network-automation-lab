"""Read-only MCP service for Arista EOS eAPI in an isolated lab."""
import os
from pathlib import Path
import httpx
import yaml
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("eos-network-observability")
SHOW = {
    "interfaces": "show interfaces status",
    "errors": "show interfaces counters errors",
    "bgp": "show ip bgp summary",
    "evpn": "show bgp evpn summary",
    "vxlan": "show vxlan vni",
    "mlag": "show mlag",
    "routes": "show ip route summary",
}

def devices():
    filename = Path(os.getenv("EOS_DEVICES_FILE", "devices.example.yml"))
    entries = yaml.safe_load(filename.read_text(encoding="utf-8"))["devices"]
    if not isinstance(entries, dict):
        raise ValueError("devices must be a mapping")
    return entries

@mcp.tool()
def list_devices() -> list[str]:
    """List configured devices."""
    return sorted(devices())

@mcp.tool()
async def device_health(device: str, check: str = "interfaces") -> dict:
    """Run an explicitly allowlisted EOS show check."""
    configured = devices()
    if device not in configured:
        raise ValueError("Device not in configured allowlist")
    if check not in SHOW:
        raise ValueError("Unsupported show check")
    endpoint = str(configured[device]).rstrip("/")
    if not endpoint.startswith("https://"):
        raise ValueError("HTTPS required")
    user = os.environ["EOS_USERNAME"]
    password = os.environ["EOS_PASSWORD"]
    verify = os.getenv("EOS_VERIFY_TLS", "true").lower() == "true"
    payload = {
        "jsonrpc": "2.0", "method": "runCmds", "id": "health",
        "params": {"version": 1, "cmds": [SHOW[check]], "format": "json"},
    }
    async with httpx.AsyncClient(verify=verify, timeout=10.0, follow_redirects=False) as client:
        response = await client.post(f"{endpoint}/command-api", json=payload, auth=(user, password))
        response.raise_for_status()
        body = response.json()
        if "error" in body:
            return {"device": device, "check": check, "error": body["error"]}
        return {"device": device, "check": check, "result": body.get("result", [])}

if __name__ == "__main__":
    mcp.run(transport="stdio")
