# Read-only EOS MCP observability service

I expose a small, fixed set of operational queries through MCP so an assistant can examine interface/BGP/VXLAN/MLAG state without general-purpose CLI execution.

```bash
cd observability-mcp
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export EOS_USERNAME=admin EOS_PASSWORD='from-secret-store'
python server.py
```
A trusted TLS certificate and restricted eAPI user are required. The tool has no configuration-write endpoint. Run it only on a trusted host and do not expose the stdio service to untrusted remote callers.

