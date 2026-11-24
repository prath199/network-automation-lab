# Arista fabric automation

I maintain two complementary Arista network labs:

1. **[Six-switch MLAG automation](mlag-six-switch/README.md)** — three independent MLAG pairs, ten Python/Ansible operational workflows, YAML fabric source-of-truth, config rendering, read-only verification, CI and a diagram.
2. **[Arista spine-leaf EVPN-VXLAN](configs/)** — two-spine/two-leaf configuration templates with [verification steps](verify.md).

The six-switch design does not use a single six-way MLAG domain: MGT-01/02, MGT-03/04, and MGT-05/06 form three **separate** MLAG domains and cross-pair links use dedicated LACP bundles.

All examples require isolated lab validation and an approved rollback plan before any live network change.
