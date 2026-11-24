# Arista CER management MLAG — reconstructed lab

I originally built this lab to investigate switch gateway migration, MLAG, VARP, cross-switch LACP and possible L2 loops. This is a **reconstruction** of my six-switch plus host/firewall-simulator topology—not a copy of customer configurations or a PAN-OS HA emulator.

## Topology
- CER access MLAG: MGT-01 / MGT-02
- IT2 access MLAG: MGT-03 / MGT-04
- VARP gateway MLAG: MGT-05 / MGT-06
- Po49 peer-link, Po51/Po52 gateway access uplinks, Po47/Po48 simulated firewall LACP
- Two Alpine hosts on VLANs 428 and 422; Linux firewall active .253 and standby .252

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

Requires a legally obtained `ceos:4.34.9.2M` image and container-to-EOS interface mapping validation. The Alpine firewall script may need package access and suitable bonding kernel modules.

**Production warning:** The original cutover discussion highlighted unknown temporary Ethernet34 pathways, possible overlapping VARP gateway ownership, and Palo Alto HA/LACP questions. Do not treat these files as approved migration instructions. End-to-end lab behavior has not been retested from this published reconstruction.

