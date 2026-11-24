# 04 — Controlled VLAN rollout

When onboarding a new application network I want a **declarative VLAN change**, an auditable diff, and a small canary before a fleet-wide change.

## Run
```bash
cd automation/ansible
ansible-playbook 04-vlan-rollout/deploy.yml -e @04-vlan-rollout/vlans.example.yml -e approved=true --check --diff --limit eos-leaf-01
ansible-playbook 04-vlan-rollout/deploy.yml -e @04-vlan-rollout/vlans.example.yml -e approved=true --limit eos-leaf-01
```
I treat `--check` as preview only. Any rollback depends on the previous VLAN state and an approved maintenance procedure. No interface trunk, SVI or gateway is changed by this playbook.

