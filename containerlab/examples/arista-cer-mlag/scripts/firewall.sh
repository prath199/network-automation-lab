#!/bin/sh
# Linux firewall simulators, NOT Palo Alto PAN-OS HA. Requires iproute2 on the image.
# Alpine package installation needs network and may fail in offline environments.
set -eu
MODE="${1:-standby}"
apk add --no-cache iproute2 iptables >/dev/null
ip link add bond0 type bond mode 802.3ad miimon 100 lacp_rate fast
ip link set eth1 down
ip link set eth2 down
ip link set eth1 master bond0
ip link set eth2 master bond0
ip link set bond0 up
ip link set eth1 up
ip link set eth2 up
ip link add link bond0 name bond0.426 type vlan id 426
ip link set bond0.426 up
if [ "$MODE" = active ]; then
  ip addr add 10.4.26.253/24 dev bond0.426
  sysctl -w net.ipv4.ip_forward=1
  # Outbound traffic uses Containerlab's management network for lab-only NAT.
  iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
else
  ip addr add 10.4.26.252/24 dev bond0.426
fi
