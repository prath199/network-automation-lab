# Acceptance test matrix
1. Confirm physical links and /31 adjacency reachability.
2. Confirm BGP underlay sessions and Loopback0/Loopback1 routes.
3. Confirm EVPN peer status and advertised Type-2 routes.
4. Check VTEP mappings and VXLAN L2 VNI associations.
5. Test same-VLAN host connectivity across the fabric.
6. Remove one uplink, rerun convergence and MAC reachability checks.
7. Restore the link and record expected versus actual output.

