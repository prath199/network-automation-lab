# 05 — IOS-XE software upgrade preflight

Before a scheduled switch upgrade I capture software and platform state, verify free storage and collect boot and stack details. I deliberately **do not reboot or install a new image** from this initial use case; a safe deployment requires platform-specific ISSU/reload decision-making, redundancy testing and console rollback access.

```bash
cd automation/ansible
ansible-playbook 05-iosxe-switch-upgrade/preflight.yml --limit iosxe-edge-01
```
Review the captured command outputs with the appropriate Cisco release notes and image checksums, and obtain a change ticket before proceeding with a separate approved upgrade runbook.

