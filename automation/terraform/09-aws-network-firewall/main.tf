provider "aws" { region = var.aws_region }
variable "aws_region" { type = string }
variable "vpc_id" { type = string }
variable "inspection_subnet_ids" {
  type = list(string)
  validation {
    condition = length(var.inspection_subnet_ids) >= 2 && length(distinct(var.inspection_subnet_ids)) == length(var.inspection_subnet_ids)
    error_message = "Provide at least two distinct inspection subnets in distinct AZs."
  }
}
resource "aws_networkfirewall_firewall_policy" "inspection" {
  name = "netops-inspection-policy"
  firewall_policy {
    stateless_default_actions = ["aws:forward_to_sfe"]
    stateless_fragment_default_actions = ["aws:forward_to_sfe"]
  }
  tags = { ManagedBy = "Terraform" }
}
resource "aws_networkfirewall_firewall" "inspection" {
  name = "netops-inspection"
  vpc_id = var.vpc_id
  firewall_policy_arn = aws_networkfirewall_firewall_policy.inspection.arn
  dynamic "subnet_mapping" {
    for_each = toset(var.inspection_subnet_ids)
    content { subnet_id = subnet_mapping.value }
  }
  delete_protection = true
  subnet_change_protection = true
  firewall_policy_change_protection = true
  tags = { ManagedBy = "Terraform" }
}
output "firewall_arn" { value = aws_networkfirewall_firewall.inspection.arn }

