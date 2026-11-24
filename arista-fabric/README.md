# Arista EOS spine-leaf EVPN/VXLAN starter

I model a small 2-spine/2-leaf CLOS fabric with routed /31 links, iBGP/eBGP design decisions, VTEP loopbacks and VXLAN encapsulation. This track is independent of the Cisco Nexus EVPN project under `evpn-deployment/`.

## Run
Load a licensed cEOSLab image and deploy `containerlab/topology.clab.yml`. Match the container Ethernet interface numbering to the EOS interface mapping before applying generated configs.

## Verification
```
show interfaces status
show ip bgp summary
show ip route
show bgp evpn summary
show bgp evpn route-type mac-ip
show vxlan vni
show vxlan address-table
```
The configs are deliberately preliminary reference examples, not tested reference designs. Verify all underlay routes and EVPN route reflection/next-hop behavior before testing host reachability.

