# Cisco Nexus VXLAN EVPN deployment

My existing repository [vxlan-evpn-iac](https://github.com/prath199/vxlan-evpn-iac) contains Ansible roles, YAML-based fabric definition, Nexus underlay and overlay deployment, validation playbooks and a Cisco Modeling Labs topology.

This folder contains a **pinned Git submodule** at `cisco-nexus-vxlan-evpn/`, referencing commit `1e86a650bad66b33e620d3518e1486aeeeee447a`. To fetch its code:
```bash
git clone --recurse-submodules https://github.com/prath199/network-automation-lab.git
# or from a clone:
git submodule update --init --recursive
```
The source repository's MIT license and Matthew Rich attribution remain in the submodule. The Nexus project is a separate reference implementation; it is not the Arista EVPN lab.

