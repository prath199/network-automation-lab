# 08 — Multi-AZ AWS VPC

I use Terraform to build a two-AZ VPC with public and private subnets. This is a foundation for network teams deploying workloads while maintaining reviewed network CIDRs as versioned data.

## Run
```bash
cd automation/terraform/08-aws-vpc
terraform init
terraform fmt -check
terraform validate
terraform plan -var-file=terraform.tfvars.example
```
For a production rollout I require an encrypted remote state backend, account-role isolation, PR-reviewed plan, CIDR/IPAM collision checks and a documented destroy/rollback path. This example does not create internet or NAT gateways, so private subnets have no egress by default.

