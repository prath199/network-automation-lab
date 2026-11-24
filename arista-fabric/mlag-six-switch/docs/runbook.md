# Six-switch Arista MLAG operations runbook

My topology has **three independent MLAG domains**, not a six-switch MLAG system. Each pair has Po49 as an isolated control peer-link carrying only VLAN 4094. MGT-05/06 use Po51 to connect the CER access pair and Po52 to connect the IT2 access pair. Distinct Linux firewall-simulator bonds use Po47 and Po48.

## Ten automated scenarios

| # | Scenario | Code | Change impact |
|---|---|---|---|
| 01 | Validate YAML source of truth | python/validate.py | none |
| 02 | Render six-device, stage-separated configs | python/render.py | none |
| 03 | Capture pre-change backups | ansible/03_backup.yml | read only |
| 04 | MLAG readiness checks | ansible/04_preflight.yml | read only |
| 05 | Configure VLAN4094/Po49 peer links | ansible/05_peerlink.yml | high impact |
| 06 | Configure three MLAG control domains | ansible/06_mlag.yml | high impact |
| 07 | Configure cross-pair LACP bundles | ansible/07_bundles.yml | high impact |
| 08 | Configure gateway VARP/SVIs | ansible/08_gateway.yml | high impact |
| 09 | Collect operational verification | ansible/09_verify.yml | read only |
| 10 | Detect device configuration drift | python/drift.py | read only |

## Safe deployment sequence

```bash
cd arista-fabric/mlag-six-switch
python -m pip install -r requirements.txt
python python/validate.py
python python/render.py
cd ansible
ansible-galaxy collection install -r requirements.yml
ansible-playbook 03_backup.yml
ansible-playbook 04_preflight.yml
ansible-playbook 05_peerlink.yml -e approved=true --check --diff --limit MGT-01,MGT-02
# Only after review of the generated diff and on an isolated test lab:
ansible-playbook 05_peerlink.yml -e approved=true --limit MGT-01,MGT-02
ansible-playbook 06_mlag.yml -e approved=true --limit MGT-01,MGT-02
ansible-playbook 09_verify.yml --limit MGT-01,MGT-02
```

Repeat pair-by-pair before enabling cross-pair Port-Channels. Use 07 then 08 only after explicit link and control-plane validation. These high-impact changes should be applied over out-of-band connectivity with a rollback plan; the scripts never trigger write memory automatically.

## Acceptance tests
- `show mlag`: Active, Connected, peer-link Up on all three pairs
- `show port-channel summary`: expected Ethernet members bundled
- `show lacp neighbor`: remote system IDs stable and matching MLAG pairs
- `show spanning-tree`: no unexpected alternate forwarding path
- `show ip interface brief`: SVI4094 peer IPs and gateway SVIs correct
- `show mac address-table`: no duplicate/churning virtual MAC
- HOST-A VLAN428 to HOST-B VLAN422 reachability with correct routing
- Firewall-facing VLAN426 tags and next-hop validated independently

This is a public **lab implementation**; it has not been deployed on customer equipment. Real migrations must resolve the Ethernet34 temporary-path question, firewall tagging/HA/LACP, and gateway handoff ownership.
