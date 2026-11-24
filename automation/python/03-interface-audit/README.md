# 03 — Fleet interface auditing

I collect interface status and error counters from hundreds of Cisco IOS-XE and Arista EOS switches using bounded SSH concurrency and one report entry per device.

## Run
```bash
cd automation
export PYTHONPATH=python NETOPS_USERNAME=admin
python python/03-interface-audit/audit.py --inventory data/devices.example.yml --output outputs/interfaces.json --workers 12
```
I use this as an input to a later baseline and alerting platform, not a stand-alone statement of network health. Vendor CLI output needs platform-specific parsing for normalized metrics.

