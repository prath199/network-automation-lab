variable "fabric_name" { type = string; default = "lab-fabric" }
variable "devices" {
  type = map(object({ role = string, mgmt_ip = string, loopback0 = string, asn = number }))
  default = {
    spine1 = { role = "spine", mgmt_ip = "172.20.20.11", loopback0 = "10.255.0.1", asn = 65000 }
    spine2 = { role = "spine", mgmt_ip = "172.20.20.12", loopback0 = "10.255.0.2", asn = 65000 }
    leaf1  = { role = "leaf", mgmt_ip = "172.20.20.21", loopback0 = "10.255.0.11", asn = 65101 }
    leaf2  = { role = "leaf", mgmt_ip = "172.20.20.22", loopback0 = "10.255.0.12", asn = 65102 }
  }
  validation {
    condition = alltrue([for d in values(var.devices) : contains(["spine", "leaf"], d.role) && d.asn >= 1 && d.asn <= 4294967295])
    error_message = "Use spine/leaf roles and valid BGP ASNs."
  }
}
variable "vlans" {
  type = map(object({ name = string, vni = number, vrf = string }))
  default = {
    "100" = { name = "APP", vni = 10100, vrf = "TENANT-A" }
    "200" = { name = "DB", vni = 10200, vrf = "TENANT-A" }
  }
  validation {
    condition = alltrue([for k, v in var.vlans : can(tonumber(k)) && tonumber(k) >= 1 && tonumber(k) <= 4094 && v.vni >= 1 && v.vni <= 16777215]) && length(distinct([for v in values(var.vlans) : v.vni])) == length(var.vlans)
    error_message = "VLAN IDs must be 1..4094; VNI values must be unique."
  }
}
variable "links" {
  type = list(object({ a = string, a_port = string, b = string, b_port = string, a_ip = string, b_ip = string }))
  default = [
    { a = "spine1", a_port = "Ethernet1", b = "leaf1", b_port = "Ethernet1", a_ip = "10.0.0.0/31", b_ip = "10.0.0.1/31" },
    { a = "spine2", a_port = "Ethernet1", b = "leaf1", b_port = "Ethernet2", a_ip = "10.0.0.2/31", b_ip = "10.0.0.3/31" },
    { a = "spine1", a_port = "Ethernet2", b = "leaf2", b_port = "Ethernet1", a_ip = "10.0.0.4/31", b_ip = "10.0.0.5/31" },
    { a = "spine2", a_port = "Ethernet2", b = "leaf2", b_port = "Ethernet2", a_ip = "10.0.0.6/31", b_ip = "10.0.0.7/31" }
  ]
}
