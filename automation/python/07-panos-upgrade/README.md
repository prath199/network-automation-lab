# 07 — PAN-OS software upgrade readiness and approval gate

I don't automate HA failover and software activation without confirming supported upgrade paths, peer synchronization, session state, maintenance access and approved rollback. This first workflow reads the firewall version and HA state, and only emits an upgrade plan.

## Run
```bash
cd automation
export PANOS_API_KEY_FW01='from-secret-manager'
python python/07-panos-upgrade/upgrade.py --host 192.0.2.101 --api-key-env PANOS_API_KEY_FW01 --target-version 11.2.5 --ca-bundle /etc/ssl/certs/ca-certificates.crt
```
**No upgrade installation or restart is executed.** An operator must consult vendor-specific upgrade-path guidance and review HA behavior before using a separate change-controlled deployment process.

