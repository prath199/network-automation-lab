# Validation checklist
```
show interfaces status
show ip interface brief
show ip bgp summary
show ip route
show bgp evpn summary
show bgp evpn route-type mac-ip
show vxlan vni
show vxlan address-table
```
Verify underlay reachability first, then EVPN adjacencies and VNI association; finally ping from host1 to host2. Save outputs for regression comparisons. Do not interpret the existence of config templates as proof of a passing lab.
