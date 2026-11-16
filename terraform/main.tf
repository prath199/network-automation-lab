locals {
  inventory = { fabric = var.fabric_name, devices = var.devices }
  addressing = { for name, d in var.devices : name => { mgmt_ip = d.mgmt_ip, loopback0 = d.loopback0 } }
  vlan_vni_plan = { vlans = var.vlans }
  bgp_peer_plan = { for name, d in var.devices : name => {
    local_asn = d.asn
    overlay_peers = d.role == "leaf" ? { for sn, sp in var.devices : sn => sp.loopback0 if sp.role == "spine" } : { for ln, lf in var.devices : ln => lf.loopback0 if lf.role == "leaf" }
  } }
  port_map = { links = var.links }
  artifacts = {
    "01-device-inventory.json" = local.inventory
    "02-ip-addressing.json" = local.addressing
    "03-vlan-vni-plan.json" = local.vlan_vni_plan
    "04-bgp-peer-plan.json" = local.bgp_peer_plan
    "05-port-map.json" = local.port_map
  }
}
resource "local_file" "plan" {
  for_each = local.artifacts
  filename = "${path.module}/generated/${each.key}"
  content = jsonencode(each.value)
  file_permission = "0644"
}
output "generated_paths" { value = [for f in local_file.plan : f.filename] }
