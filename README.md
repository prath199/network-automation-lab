# Network Automation Lab

I built this repository to demonstrate practical network automation across Cisco IOS-XE, Arista EOS, Palo Alto PAN-OS, and AWS. YAML is my source of truth until I integrate NetBox.

## Start here

- [10 operational use cases](automation/README.md): Ansible, Python, Terraform with scenario-specific code and documentation.
- [Arista EVPN](arista-fabric/README.md) and [Containerlab](containerlab/README.md).
- [Cisco Nexus VXLAN EVPN](evpn-deployment/README.md): pinned Git submodule referencing my separate EVPN repository.
- [MCP Network Observability](observability-mcp/README.md).

All IP addresses in inventory examples are illustrative. Operations that modify devices or cloud infrastructure must be reviewed and tested in an isolated environment. My offline tests are not a substitute for validation on physical devices or production APIs.
