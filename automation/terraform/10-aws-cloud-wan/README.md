# 10 — AWS Cloud WAN core network

I declare Cloud WAN global network resources and a network policy for two isolated segments: infrastructure and applications. This is the foundation for multi-region inter-VPC transit. I intentionally avoid attaching an arbitrary production VPC.

## Run
```bash
cd automation/terraform/10-aws-cloud-wan
terraform init && terraform validate
terraform plan -var-file=terraform.tfvars.example
```
Publishing a Cloud WAN core network policy requires a separate reviewed change. Before adding VPC attachments, validate attachments, association behavior, route propagation, subnet selection, segment isolation and account-level permissions. Cloud WAN incurs AWS costs.

