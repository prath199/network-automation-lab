# Arista CER management MLAG lab — reconstructed example

**Source:** reconstructed from your November 2026 Containerlab conversation and cutover review. Not a byte-for-byte copy of `~/network-labs/arista-cer`, and not production-approved.

**Separate from** `containerlab/topology.clab.yml` (which models a new spine-leaf EVPN fabric).

## Layout
- Six cEOSLab nodes: MGT-01/02 CER access MLAG, MGT-03/04 IT2 access MLAG, MGT-05/06 gateway MLAG.
- Po49 is each pair's MLAG peer-link.
- Gateway pair Po51 connects CER access, Po52 connects IT2.
- Po47 and Po48 connect **separate** simulated Linux firewall LACP bonds.
- HOST-A (VLAN 428) and HOST-B (VLAN 422) test routed reachability across gateway SVIs.
- Gateway VARP addresses across VLANs 50, 422, 424, 426, 428, 430 and 432.
- Firewall next-hop 10.4.26.253 exists only on the primary Linux simulator; standby has .252 **without HA failover**.
- `eth7 -> Ethernet47`, `eth8 -> Ethernet48`; `eth1..eth6 -> Ethernet49..54`.

## Run
```bash
cd containerlab/examples/arista-cer-mlag
sudo containerlab deploy -t topology.clab.yml
sudo containerlab inspect -t topology.clab.yml
docker exec clab-arista-cer-portfolio-MGT-05 Cli -p 15 -c 'show mlag'
docker exec clab-arista-cer-portfolio-MGT-06 Cli -p 15 -c 'show port-channel summary'
docker exec clab-arista-cer-portfolio-HOST-A ping -c 3 10.4.22.100
sudo containerlab destroy -t topology.clab.yml
```
Image `ceos:4.34.9.2M` must be legally obtained and imported. Linux simulation expects outbound package access; without it the firewall setup will fail. Interface mapping and EOS configuration syntax need verification against your image, and Linux LACP bonds may need additional kernel support.

## Differences from the production migration
This example deliberately excludes production secrets, existing startup-config exports and the unknown Ethernet34 temporary path. It is **not** a valid Palo Alto HA test. The historic runbook flagged potential duplicate VARP gateway ownership, unknown Ethernet34 wiring, and inconsistent proposed VLAN426 switch IP addresses; resolve these separately before any cutover. Do not use these synthetic configs as a source of truth for real cabling.

## Checks
Run `show mlag`, `show mlag interfaces`, `show port-channel summary`, `show lacp neighbor`, `show spanning-tree`, `show ip route`, and host pings. End-to-end tests have **not** been executed on this GitHub version.
