# Security
This is an **isolated lab** implementation, not a production change system.
- Never commit credentials, private configurations, SSH keys, Terraform state or tokens.
- Never aim sample inventory at customer or production devices.
- Ansible changes require explicit `-e apply_changes=true`; preview with `--check --diff`.
- The MCP server uses a read-only show-command allowlist, and HTTPS eAPI.
- Keep TLS verification enabled; disabling it is only appropriate for disposable labs.
- Validate EOS interface mappings and routing features before activating configurations.
