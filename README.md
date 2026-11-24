# Network Automation Lab

I use network automation to turn repeatable Cisco IOS-XE, Arista EOS, Palo Alto PAN-OS and AWS network operations into reviewable code. The first source of truth is YAML; a NetBox integration is planned.

## Portfolio
- [Ten network automation scenarios](automation/README.md) — each with a practical README, code and input files.
- [Ansible use cases](automation/ansible) — configuration backup, guarded VLAN deployment, IOS-XE upgrade preflight.
- [Python use cases](automation/python) — drift detection, interface audit, PAN-OS backups and upgrade readiness.
- [Terraform use cases](automation/terraform) — AWS VPC, Network Firewall, Cloud WAN.
- [Cisco Nexus VXLAN EVPN](evpn-deployment/README.md) — pinned Git submodule to my [existing repository](https://github.com/prath199/vxlan-evpn-iac).
- [Containerlab](containerlab/README.md) — virtual Arista networking lab.

These examples have **not been validated across production fleets**. Read-only operations, maintenance approval, version-specific checks and sandbox Terraform plans are the starting point. Never commit real credentials or configuration backups.

[Security](SECURITY.md) · [Roadmap](ROADMAP.md)
