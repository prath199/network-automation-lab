# 01 — Fleet configuration backups

I use this playbook to collect Cisco IOS-XE and Arista EOS configurations before maintenance windows and for day-2 change evidence.

**Topology:** NOC runner → SSH → network devices. Inventory: `../inventory/hosts.example.yml`.

## Run
```bash
cd automation/ansible
export NETOPS_USERNAME=admin NETOPS_PASSWORD='from-secret-store'
ansible-galaxy collection install -r requirements.yml
ansible-playbook 01-fleet-backups/backup.yml --limit iosxe
```
Backups are stored locally with restrictive permissions under an ignored `outputs/` directory. In a deployment at scale, I would move them into an encrypted object store with retention, access logging, and a scheduled backup test. The runner should have a dedicated least-privileged account and verified SSH host keys. Do not upload captured configs to Git.

