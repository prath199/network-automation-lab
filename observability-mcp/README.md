# Read-only MCP network observability

A FastMCP stdio server that queries EOS eAPI (HTTPS/JSON-RPC). Available tools: `list_devices()` and `device_health(device, check)`. Supported checks: interfaces, errors, IPv4 BGP, EVPN, VXLAN, MLAG, and route summaries. No arbitrary CLI or configuration-change endpoint.

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export EOS_USERNAME=admin
export EOS_PASSWORD='YOUR_LAB_PASSWORD'
export EOS_DEVICES_FILE=devices.example.yml
python server.py
```

Configure your MCP client to run this script using the venv Python. EOS eAPI must be enabled with HTTPS and a trusted certificate. `EOS_VERIFY_TLS=false` is only for a disposable lab. Historical collection, alerts and role-based authentication are future milestones.
