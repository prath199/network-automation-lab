# 06 — Palo Alto firewall configuration backups

I use the PAN-OS XML API to export device configuration snapshots for change evidence. The script authenticates with an API key from an environment variable and writes the response to a restricted local output folder. It does not change any firewall configuration.

## Run
```bash
cd automation
export PANOS_API_KEY_FW01='from-secret-manager'
python python/06-panos-backup/backup.py --inventory data/paloalto.example.yml --output outputs/panos --ca-bundle /etc/ssl/certs/ca-certificates.crt
```
I require certificate verification, a least-privilege account, limited access to backups and encrypted retention. Test API response handling against each PAN-OS release. Never commit exported XML into Git.

