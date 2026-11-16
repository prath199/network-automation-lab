# Containerlab topology
Two spine and two leaf Arista cEOSLab routers plus two Alpine Linux hosts.

```bash
sudo containerlab deploy -t topology.clab.yml
sudo containerlab inspect -t topology.clab.yml
sudo containerlab destroy -t topology.clab.yml
```

The topology assumes a **legally obtained** cEOSLab image imported as `ceos:4.34.9.2M`.
**Important:** Containerlab `ethN` numbering is not necessarily `EthernetN` in EOS. Verify interface mapping on your image; adapt the topology/interface mapping before loading EOS configs. Host IPs use VLAN 100 as an isolated L2 VNI test. No end-to-end connectivity has been validated yet.
