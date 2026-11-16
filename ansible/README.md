# Ansible operations — five workflows
Install `ansible-core` then `ansible-galaxy collection install -r requirements.yml`.

1. **01_backup.yml:** collect configuration backups into ignored local outputs.
2. **02_interface_audit.yml:** collect interface status and platform information.
3. **03_compliance.yml:** check the presence of NTP and remote syslog configuration.
4. **04_deploy_vlan.yml:** merge a VLAN into the EOS configuration.
5. **05_port_description.yml:** standardize an interface description.

Run from this directory, e.g. `ansible-playbook playbooks/01_backup.yml`.
For change playbooks preview with `ansible-playbook playbooks/04_deploy_vlan.yml --check --diff -e apply_changes=true`. To apply in an isolated lab, omit `--check`.
Supply secure credentials outside this repository. Verify each playbook against your specific EOS release before use.
