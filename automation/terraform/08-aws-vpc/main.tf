provider "aws" { region = var.aws_region }
variable "aws_region" { type = string }
variable "vpc_cidr" { type = string }
variable "public_subnets" { type = list(string) }
variable "private_subnets" { type = list(string) }
data "aws_availability_zones" "available" { state = "available" }
locals { azs = slice(data.aws_availability_zones.available.names, 0, 2) }
resource "aws_vpc" "network" {
  cidr_block = var.vpc_cidr
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = { Name = "netops-portfolio-vpc", ManagedBy = "Terraform" }
}
resource "aws_subnet" "public" {
  count = 2
  vpc_id = aws_vpc.network.id
  cidr_block = var.public_subnets[count.index]
  availability_zone = local.azs[count.index]
  map_public_ip_on_launch = false
  tags = { Name = "public-${count.index + 1}" }
}
resource "aws_subnet" "private" {
  count = 2
  vpc_id = aws_vpc.network.id
  cidr_block = var.private_subnets[count.index]
  availability_zone = local.azs[count.index]
  tags = { Name = "private-${count.index + 1}" }
}
output "vpc_id" { value = aws_vpc.network.id }
output "private_subnet_ids" { value = aws_subnet.private[*].id }
output "public_subnet_ids" { value = aws_subnet.public[*].id }

