provider "aws" { region = var.aws_region }
variable "aws_region" { type = string }
variable "edge_locations" {
  type = list(string)
  validation {
    condition = length(var.edge_locations) > 0
    error_message = "Provide at least one region."
  }
}
resource "aws_networkmanager_global_network" "global" {
  description = "Network automation portfolio - global network"
  tags = { ManagedBy = "Terraform" }
}
resource "aws_networkmanager_core_network" "core" {
  global_network_id = aws_networkmanager_global_network.global.id
  description = "Core network - policy requires change review"
  tags = { ManagedBy = "Terraform" }
}
locals {
  policy = {
    version = "2021.12"
    core-network-configuration = { vpn-ecmp-support = true, edge-locations = [for region in var.edge_locations : { location = region }] }
    segments = [
      { name = "infrastructure", require-attachment-acceptance = true },
      { name = "applications", require-attachment-acceptance = true }
    ]
    segment-actions = []
    attachment-policies = []
  }
}
output "core_network_id" { value = aws_networkmanager_core_network.core.id }
output "draft_policy_json" { value = jsonencode(local.policy) }

