# Safety and responsible use
This public portfolio contains **lab templates** and deliberately uses documentation-only IP ranges in inventory. Never commit credentials, tokens, customer device configurations, secrets, backups, topology with private customer details, or Terraform state.
Read-only workflows are a starting point. Mutable workloads require explicit approval, change record, tested rollback, pre/post checks, bounded concurrency, and review of vendor release notes.
AWS examples can incur costs; `terraform plan` is not approval to apply. PAN-OS and IOS-XE upgrades are not hands-off automations. 

