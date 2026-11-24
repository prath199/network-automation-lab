# Ten real-world network automation workflows
I maintain YAML inventory in `automation/data/` and split automation into Ansible, Python, and Terraform. Each use case has its own README with prerequisites, execution, validation and rollback considerations.

| # | Scenario | Implementation |
|---|---|---|
| 01 | Scheduled Cisco and Arista configuration backup | Ansible |
| 02 | Configuration drift detection against approved YAML baselines | Python |
| 03 | Fleet interface health reporting | Python |
| 04 | Controlled VLAN rollout across Arista EOS | Ansible |
| 05 | Cisco IOS-XE switch software preflight (no activation) | Ansible |
| 06 | Palo Alto configuration export | Python |
| 07 | PAN-OS upgrade planning / safety gate (no automatic failover) | Python |
| 08 | AWS multi-AZ VPC | Terraform |
| 09 | AWS Network Firewall | Terraform |
| 10 | AWS Cloud WAN core network | Terraform |

The source here is an implementation reference with **offline checks**, not a claim of production certification or battle-tested upgrade automation. Do not put passwords or running-config backups in Git. Start with read-only operations. Use CI and canary deployment before a larger rollout.

