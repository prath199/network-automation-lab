"""YAML-backed MLAG source of truth with strict topology checks."""
import ipaddress
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
def load(path=None):
    return yaml.safe_load(Path(path or ROOT / "data/fabric.yml").read_text(encoding="utf-8"))

def validate(data):
    errors = []
    pairs = data.get("pairs", {})
    devices = data.get("devices", {})
    fabric = data.get("fabric", {})
    vlans = data.get("vlans", {})
    seen = set()
    if len(pairs) != 3 or len(devices) != 6:
        errors.append("Expected exactly 3 MLAG pairs / 6 switches")
    for domain, pair in pairs.items():
        members = pair.get("nodes", [])
        ips = pair.get("peer_ips", [])
        if len(members) != 2 or len(set(members)) != 2 or len(ips) != 2:
            errors.append(f"{domain}: requires exactly two different members and peer IPs")
            continue
        try:
            endpoints = [ipaddress.ip_interface(ip) for ip in ips]
            if endpoints[0].network != endpoints[1].network or endpoints[0].ip == endpoints[1].ip:
                errors.append(f"{domain}: peer IPs must share one subnet and differ")
        except ValueError:
            errors.append(f"{domain}: invalid peer IP")
        for node in members:
            if node in seen or node not in devices:
                errors.append(f"{domain}: duplicate or unknown node {node}")
            seen.add(node)
            if node in devices and devices[node].get("pair") != domain:
                errors.append(f"{node}: pair reference mismatches {domain}")
        b0 = devices.get(members[0], {}).get("bundles", [])
        b1 = devices.get(members[1], {}).get("bundles", [])
        if {int(x["id"]) for x in b0} != {int(x["id"]) for x in b1}:
            errors.append(f"{domain}: partners have different bundle IDs")
    if set(devices) != seen:
        errors.append("Every device must belong to exactly one pair")
    if int(fabric.get("mlag_vlan", -1)) in set(int(x) for x in fabric.get("allowed_vlans", [])):
        errors.append("MLAG control VLAN cannot be on ordinary trunks")
    if set(map(int, fabric.get("allowed_vlans", []))) != set(map(int, vlans)):
        errors.append("VLAN catalog must match allowed VLANs")
    control_addresses, mgmt_addresses, all_svi = [], [], []
    for name, dev in devices.items():
        if dev.get("role") not in ("gateway", "access"):
            errors.append(f"{name}: invalid role")
        mgmt_addresses.append(dev.get("mgmt"))
        ports = ["Ethernet49", "Ethernet50"]
        port_channels = [49]
        for b in dev.get("bundles", []):
            ports.extend(b["ports"])
            port_channels.append(int(b["id"]))
            if int(b["id"]) == 49:
                errors.append(f"{name}: peer-link reserved Po49")
            if not set(map(int, b.get("vlans", fabric.get("allowed_vlans", [])))).issubset(set(map(int, vlans))):
                errors.append(f"{name}: undefined VLAN on bundle")
        for access in dev.get("host_access", []):
            ports.append(access["port"])
            if int(access["vlan"]) not in vlans:
                errors.append(f"{name}: host access VLAN undefined")
        if len(ports) != len(set(ports)) or len(port_channels) != len(set(port_channels)):
            errors.append(f"{name}: duplicate physical port or bundle ID")
        if dev.get("role") == "gateway":
            if set(map(int, dev.get("svi_ips", {}))) != set(map(int, vlans)):
                errors.append(f"{name}: missing gateway SVI")
            all_svi.extend(dev.get("svi_ips", {}).values())
        else:
            if "svi_ips" in dev:
                errors.append(f"{name}: access switches should not own gateway SVIs")
            all_svi.append(dev.get("access_mgmt_ip", ""))
    if len(set(mgmt_addresses)) != len(mgmt_addresses):
        errors.append("Duplicate device management address")
    for s in all_svi:
        try:
            ipaddress.ip_interface(s)
        except ValueError:
            errors.append(f"Invalid SVI address {s}")
    if len({str(ipaddress.ip_interface(s).ip) for s in all_svi if s}) != len(all_svi):
        errors.append("Duplicate SVI IP addresses")
    for vlan, spec in vlans.items():
        try:
            ipaddress.ip_address(spec["gateway"])
            if not 1 <= int(vlan) <= 4094 or not 1 <= int(spec["prefix"]) <= 32:
                raise ValueError("VLAN or mask invalid")
            for dev in devices.values():
                if dev.get("role") == "gateway":
                    svi = ipaddress.ip_interface(dev["svi_ips"][vlan])
                    if svi.network.prefixlen != int(spec["prefix"]) or ipaddress.ip_address(spec["gateway"]) not in svi.network:
                        errors.append(f"VLAN {vlan}: SVI/gateway subnet mismatch")
        except (ValueError, KeyError):
            errors.append(f"VLAN {vlan}: invalid gateway, prefix or missing SVI")
    if errors:
        raise ValueError("\n".join(errors))
    return True

def peer_info(data, node):
    dev = data["devices"][node]
    pair = data["pairs"][dev["pair"]]
    index = pair["nodes"].index(node)
    return pair["peer_ips"][index], pair["peer_ips"][1-index].split("/")[0]
