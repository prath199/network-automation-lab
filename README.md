# Network Automation Lab

Practical network engineering automation projects using **Ansible**, **Terraform**, **Arista EOS EVPN-VXLAN**, **Containerlab**, and a **read-only MCP observability server**.

> **Lab-only reference implementation.** Validate EOS versions, interface mapping, routing policy, image licensing, and credentials before any deployment. Never run sample changes against production without review.

## Projects

| Project | Purpose |
| --- | --- |
| [Ansible](ansible/README.md) | Five day-2 network operations: backups, interface audit, compliance, VLAN deployment, port descriptions |
| [Terraform](terraform/README.md) | Five infrastructure-intent outputs: inventory, IP addressing, VLAN/VNI mapping, BGP peers, port mapping |
| [Arista Fabric](arista-fabric/README.md) | 2-spine / 2-leaf EVPN-VXLAN example |
| [Containerlab](containerlab/README.md) | Repeatable virtual fabric topology |
| [MCP Observability](observability-mcp/README.md) | Read-only EOS eAPI diagnostic tools |

## Getting started

1. Clone the repository.
2. Install Containerlab and a licensed Arista cEOSLab image.
3. Review topology and EOS interface mapping before deployment.
4. Start with read-only Ansible tasks; run change playbooks in check mode.
5. Use Terraform for reviewable infrastructure *intent* (not direct device provisioning).
6. Configure the MCP server through environment variables; do not commit credentials.

[Roadmap](ROADMAP.md) · [Security](SECURITY.md)

Inspired by the IaC design principles in [mrichinfinite/vxlan-evpn-iac](https://github.com/mrichinfinite/vxlan-evpn-iac), adapted independently for an Arista EOS lab.
