# Terraform network intent
**Five reviewable infrastructure-as-code deliverables** (JSON outputs under `generated/`):
1. Device inventory
2. Management and loopback IP addressing
3. VLAN/VNI/VRF allocation
4. BGP overlay neighbor intent
5. Spine-leaf physical port mapping

Run `terraform init && terraform fmt -check && terraform validate && terraform plan`; `terraform apply` generates local JSON, **not switch configurations**. Keep state local and out of Git. A later phase can integrate a supported device provider or NetBox.
