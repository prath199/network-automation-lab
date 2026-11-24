#!/usr/bin/env python3
"""Use case 02: generate stage-separated, deterministic Arista EOS configs."""
import argparse
from pathlib import Path
from model import load, peer_info, validate, ROOT

STAGES = ("peerlink", "mlag", "bundles", "gateway")

def render_node(data, node):
    dev = data["devices"][node]
    f = data["fabric"]
    myip, peerip = peer_info(data, node)
    peerlink = [
        f"vlan {f['mlag_vlan']}",
        "   name MLAG-PEER",
        "   trunk group MLAG",
        "no spanning-tree vlan-id 4094",
        "interface Port-Channel49",
        "   description MLAG CONTROL - ISOLATED",
        "   switchport mode trunk",
        "   switchport trunk group MLAG",
        "interface Ethernet49",
        "   channel-group 49 mode active",
        "interface Ethernet50",
        "   channel-group 49 mode active",
        "interface Vlan4094",
        f"   ip address {myip}",
    ]
    mlag = [
        "mlag configuration",
        f"   domain-id {dev['pair']}",
        "   local-interface Vlan4094",
        f"   peer-address {peerip}",
        "   peer-link Port-Channel49",
    ]
    bundles = []
    for vid, info in sorted(data["vlans"].items()):
        bundles.extend([f"vlan {vid}", f"   name {info['name']}"])
    for b in sorted(dev.get("bundles", []), key=lambda b:int(b["id"])):
        vlans = ",".join(map(str, sorted(b.get("vlans", f["allowed_vlans"]))))
        bundles.extend([f"interface Port-Channel{b['id']}", f"   description {b['description']}",
                        "   switchport mode trunk", f"   switchport trunk allowed vlan {vlans}",
                        f"   mlag {b['id']}"])
        for port in b["ports"]:
            bundles.extend([f"interface {port}", f"   channel-group {b['id']} mode active"])
    for acc in dev.get("host_access", []):
        bundles.extend([f"interface {acc['port']}", f"   switchport access vlan {acc['vlan']}",
                        "   spanning-tree portfast"])
    gw = []
    if dev["role"] == "gateway":
        gw.extend(["ip routing", f"ip virtual-router mac-address {f['virtual_mac']}"])
        for vid, ip in sorted(dev["svi_ips"].items()):
            gw.extend([f"interface Vlan{vid}", f"   ip address {ip}",
                       f"   ip virtual-router address {data['vlans'][vid]['gateway']}"])
        gw.append(f"ip route 0.0.0.0/0 {f['default_next_hop']}")
    else:
        gw.extend(["no ip routing", "interface Vlan426",
                   f"   ip address {dev['access_mgmt_ip']}",
                   "ip default-gateway 10.4.26.1"])
    return dict(zip(STAGES, (peerlink, mlag, bundles, gw)))

def render(data, output):
    validate(data)
    output = Path(output)
    result = {}
    for node in sorted(data["devices"]):
        result[node] = render_node(data,node)
        for stage, lines in result[node].items():
            path = output / stage / (node + ".cfg")
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text("! Generated from data/fabric.yml - lab use only\n" + "\n".join(lines) + "\n",
                            encoding="utf-8")
    return result

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--output",default=str(ROOT / "output"))
    p.add_argument("--source",default=str(ROOT / "data/fabric.yml"))
    args=p.parse_args()
    result=render(load(args.source),args.output)
    print(f"Generated {len(result)*len(STAGES)} stage files for {len(result)} nodes in {args.output}")
