# 09 — AWS Network Firewall

I use a Terraform-managed firewall policy and firewall endpoints to create a central inspection boundary in a VPC. This example deliberately does not change route tables: incorrect insertion of inspection paths can break applications or create asymmetric routing.

## Run
```bash
cd automation/terraform/09-aws-network-firewall
terraform init && terraform validate
terraform plan -var-file=terraform.tfvars.example
```
Before a live deployment I verify subnet isolation, IGW/TGW routing, availability zones, rule order, logging destinations, and cost. Policy uses a stateless default action that forwards to the stateful engine; explicitly configure stateful rules before production traffic insertion.

