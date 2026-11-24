"""Allowlisted read-only EOS eAPI commands presented as MCP tools."""
import os
from pathlib import Path
import httpx
import yaml
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("eos-observability")
CHECKS = {
  "interfaces": "show interfaces status",
  "errors": "show interfaces counters errors",
  "bgp": "show ip bgp summary",
  "evpn": "show bgp evpn summary",
  "vxlan": "show vxlan vni",
  "mlag": "show mlag",
  "routes": "show ip route summary"
}
def inventory():
    data = yaml.safe_load(Path(os.getenv("EOS_DEVICES_FILE", "devices.example.yml")).read_text())
    return data["devices"]

@mcp.tool()
def list_devices() -> list[str]:
    """Show the known EOS nodes."""
    return sorted(inventory())

@mcp.tool()
async def show_health(device: str, check: str = "interfaces") -> dict:
    """Execute one preapproved show command against an allowlisted device."""
    nodes = inventory()
    if device not in nodes or check not in CHECKS:
        raise ValueError("Unknown device or show check")
    endpoint = nodes[device].rstrip("/")
    if not endpoint.startswith("https://"):
        raise ValueError("TLS endpoint required")
    payload = {"jsonrpc": "2.0", "id": "health", "method": "runCmds",
               "params": {"version": 1, "cmds": [CHECKS[check]], "format": "json"}}
    async with httpx.AsyncClient(timeout=15, verify=True, follow_redirects=False) as client:
        response = await client.post(endpoint + "/command-api", json=payload,
                                     auth=(os.environ["EOS_USERNAME"], os.environ["EOS_PASSWORD"]))
        response.raise_for_status()
        result = response.json()
    if "error" in result:
        raise RuntimeError(f"eAPI error: {result['error']}")
    return {"device": device, "check": check, "result": result.get("result", [])}
if __name__ == "__main__":
    mcp.run(transport="stdio")

