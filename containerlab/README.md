# Containerlab examples

The labs are intentionally separated:

- `topology.clab.yml`: simple Arista spine-leaf fabric.
- `examples/arista-cer-mlag/topology.clab.yml`: reconstructed six-switch management MLAG plus two hosts and two Linux firewall simulations.

For an isolated deployment with a licensed cEOSLab image:
```bash
cd containerlab
sudo containerlab deploy -t topology.clab.yml
sudo containerlab inspect -t topology.clab.yml
sudo containerlab destroy -t topology.clab.yml
```

The management MLAG topology reproduces design concepts from prior experiments but does not prove real Palo Alto HA support or production cutover safety.

