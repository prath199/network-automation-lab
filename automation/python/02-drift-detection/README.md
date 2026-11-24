# 02 — Configuration drift detection

I compare read-only running configs with approved baseline configuration text, then produce per-device unified diffs. This makes unexpected configuration changes visible without automatically overwriting legitimate emergency changes.

## Run
```bash
cd automation
export PYTHONPATH=python NETOPS_USERNAME=admin
export NETOPS_IOS_PASSWORD='from-secret-store' NETOPS_EOS_PASSWORD='from-secret-store'
python python/02-drift-detection/drift.py --inventory data/devices.example.yml --baselines python/02-drift-detection/baselines --output outputs/drift.json
```
Baseline files must be approved, normalized and stored securely (they may include secrets). No CLI configuration changes are made. Normalize platform timestamps before approving a baseline.

