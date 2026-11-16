# Arista EVPN-VXLAN learning fabric
A two-spine/two-leaf reference layout with /31 routed uplinks, eBGP underlay and staged EVPN overlay. Leaf VTEPs advertise VLAN 100 / VNI 10100. This is a **lab scaffold**—not a verified production design.

## Stages
1. Confirm actual cEOS interface mapping and load device configs.
2. Verify physical links and /31 addresses.
3. Verify underlay eBGP and loopback reachability.
4. Verify EVPN peers, VXLAN VNI and MAC learning.
5. Verify VLAN 100 host-to-host connectivity.

Spine ASN 65000; leaves ASN 65101 and 65102. Check command syntax and eBGP overlay route propagation for your EOS release; the provided templates require integration testing. See `verify.md`.
