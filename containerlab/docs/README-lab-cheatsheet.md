# Containerlab + Arista + Docker + Bash — Lab Cheatsheet

> **Scope:** Practical quick reference for my local ten-node Arista management-network lab (`arista-cer-six`). The public repository's `containerlab/topology.clab.yml` is a **different, smaller example topology**; do not run commands below against it without adapting the node names, links, and addressing.
>
> **Safety:** This is a synthetic training lab. Never publish production credentials or customer configurations. Commands such as `destroy`, `redeploy --cleanup`, `docker rm`, `ip addr flush`, or changing a default route may interrupt or delete lab state.

## 1. Project overview

Local WSL2 directory: `~/network-labs/arista-cer/`.

| Component | Role |
|---|---|
| MGT-01/MGT-02 | Arista access MLAG pair |
| MGT-03/MGT-04 | Arista access MLAG pair |
| MGT-05/MGT-06 | Arista gateway MLAG pair (VARP/SVIs) |
| HOST-A | Alpine test host in VLAN428, `10.4.28.100/23` |
| HOST-B | Alpine test host in VLAN422, `10.4.22.100/23` |
| LINUX-PA-01 | **Linux firewall simulator**, active forwarding/NAT via VLAN426 |
| LINUX-PA-02 | **Linux firewall simulator**, standby/non-forwarding |

PA-01/02 are **not PAN-OS firewalls** and do **not** implement automatic Palo Alto HA. VLAN426 next-hop in the simulation: `10.4.26.253`.

Local key files:

```text
~/network-labs/arista-cer/
├── cer-ten-node.clab.yml
├── configs/interface-mapping.json
├── scripts/hosts/host-a.sh
├── scripts/hosts/host-b.sh
├── scripts/routers/router-setup.sh
└── scripts/recover-lab.sh  # only if created locally
```

## 2. Daily lab workflow

Run these from **Ubuntu WSL**, not from the EOS CLI.

```bash
cd ~/network-labs/arista-cer
pwd
ls -lah
docker ps --filter name=clab-arista-cer-six
docker ps -a --filter name=clab-arista-cer-six
docker exec clab-arista-cer-six-MGT-05 Cli -p 15 -c 'show mlag'
docker exec clab-arista-cer-six-HOST-A ip addr show eth1
docker exec clab-arista-cer-six-HOST-A ip route
docker exec clab-arista-cer-six-HOST-A ping -c 4 10.4.28.1
docker exec clab-arista-cer-six-HOST-A ping -c 4 10.4.22.100
```

## 3. Docker essentials

| Task | Command |
|---|---|
| Running containers | `docker ps` |
| All containers | `docker ps -a` |
| Images | `docker images` |
| Docker networks | `docker network ls` |
| CPU/memory | `docker stats --no-stream` |
| Start existing switch | `docker start clab-arista-cer-six-MGT-05` |
| Logs | `docker logs --tail 100 clab-arista-cer-six-MGT-05` |
| Inspect runtime | `docker inspect -f '{{.State.Status}} {{.State.ExitCode}} {{.State.OOMKilled}}' clab-arista-cer-six-MGT-05` |
| Interactive EOS | `docker exec -it clab-arista-cer-six-MGT-05 Cli -p 15` |
| Interactive Linux | `docker exec -it clab-arista-cer-six-HOST-A sh` |
| One EOS command | `docker exec clab-arista-cer-six-MGT-05 Cli -p 15 -c 'show mlag'` |
| Copy file into container | `docker cp scripts/hosts/host-a.sh clab-arista-cer-six-HOST-A:/tmp/host-a.sh` |
| Run local script in container | `docker exec -i clab-arista-cer-six-HOST-A sh < scripts/hosts/host-a.sh` |

`-i`: stdin; `-t`: interactive terminal; `Cli -p 15`: Arista EOS privileged CLI; `-c`: execute one command.

## 4. Containerlab essentials

```bash
containerlab version
containerlab --help
containerlab deploy --help
containerlab graph --help
sudo containerlab inspect -t cer-ten-node.clab.yml

# Safely preview reconciliation after a WSL reboot
sudo containerlab deploy -t cer-ten-node.clab.yml --dry-run

# Apply only after reviewing proposed changes
sudo containerlab deploy -t cer-ten-node.clab.yml

# Diagram/visualization
sudo containerlab graph -t cer-ten-node.clab.yml
sudo containerlab graph -t cer-ten-node.clab.yml --drawio
```

Do **not** use `destroy` or `redeploy --cleanup` for routine recovery. The `graph --drawio` option depends on installed Containerlab version; check `graph --help`.

### Local cEOS interface mapping

| Container interface | EOS interface | Role |
|---|---|---|
| eth0 | Management0 | Docker management |
| eth1 | Ethernet49 | MLAG peer-link / Po49 |
| eth2 | Ethernet50 | MLAG peer-link / Po49 |
| eth3 | Ethernet51 | Access uplink |
| eth4 | Ethernet52 | Access uplink |
| eth5 | Ethernet53 | Access uplink |
| eth6 | Ethernet54 | Access uplink |
| eth7 | Ethernet47 | Firewall simulator Po47 |
| eth8 | Ethernet48 | Firewall simulator Po48 |

This mapping is lab-specific: confirm `configs/interface-mapping.json`.

## 5. Arista EOS troubleshooting

```text
show version
show running-config
show startup-config
show interfaces status
show interfaces Ethernet49
show interfaces Port-Channel49
show port-channel dense
show lacp neighbor
show mlag
show mlag config-sanity
show vlan
show interfaces trunk
show ip interface brief
show ip route
show ip arp
show mac address-table
show spanning-tree
show logging last 50
```

Healthy MLAG: `Active` / `Connected` / peer-link `Up`. For `Lowerlayerdown`, first inspect Po49 and the container's `eth1`/`eth2`; do not immediately change MLAG configuration.

All-switch check:

```bash
for sw in MGT-01 MGT-02 MGT-03 MGT-04 MGT-05 MGT-06; do
  echo "========== $sw =========="
  docker exec "clab-arista-cer-six-$sw" Cli -p 15 -c 'show mlag'
done
```

## 6. Alpine/BusyBox host IP, routes, and pings

The Alpine `alpine:3.20` BusyBox `ip` command does **not** support `ip -br addr` in our image. Use `ip addr show eth1` and `ip route`.

```bash
# Inspect HOST-A from WSL
docker exec clab-arista-cer-six-HOST-A ip addr show eth1
docker exec clab-arista-cer-six-HOST-A ip route

# Inside HOST-A only, when recovering a missing IP
ip link set eth1 mtu 1500
ip link set eth1 up
ip addr add 10.4.28.100/23 dev eth1
ip route replace default via 10.4.28.1 dev eth1

# Inside HOST-B when recovering a missing IP
ip link set eth1 mtu 1500
ip link set eth1 up
ip addr add 10.4.22.100/23 dev eth1
ip route replace default via 10.4.22.1 dev eth1
```

Avoid adding an IP twice; check first. Use an idempotent host setup script if available.

```bash
docker exec clab-arista-cer-six-HOST-A ping -c 4 10.4.28.1
docker exec clab-arista-cer-six-HOST-A ping -c 4 10.4.22.100
docker exec clab-arista-cer-six-HOST-A ping -c 4 10.4.26.253
docker exec clab-arista-cer-six-HOST-A ping -c 4 1.1.1.1
```

Docker's management default is usually `172.20.20.1` over `eth0`. For a complete forwarding-path test, ensure the route to `1.1.1.1` goes via `10.4.28.1` over `eth1` (either change the lab host's default route or add a specific `/32` route). Otherwise a successful internet ping might bypass Arista.

## 7. Linux firewall simulator and NAT

```bash
docker exec clab-arista-cer-six-LINUX-PA-01 ip -br addr
docker exec clab-arista-cer-six-LINUX-PA-01 cat /proc/net/bonding/bond0
docker exec clab-arista-cer-six-LINUX-PA-01 ip addr show bond0.426
docker exec clab-arista-cer-six-LINUX-PA-01 ip route
docker exec clab-arista-cer-six-LINUX-PA-01 sysctl net.ipv4.ip_forward
docker exec clab-arista-cer-six-LINUX-PA-01 iptables -L FORWARD -n -v
docker exec clab-arista-cer-six-LINUX-PA-01 iptables -t nat -L POSTROUTING -n -v
```

Expected: PA-01 tagged `bond0.426` address `10.4.26.253/24`; LACP bond `bond0` with `eth1/eth2`; return route toward `10.4.0.0/16` via VARP `10.4.26.1`; IP forwarding and MASQUERADE enabled. PA-02 uses `10.4.26.252/24` with forwarding disabled.

Original `router-setup.sh` was **not idempotent**: it blindly created `bond0` and appended NAT rules. Only rerun after reviewing or replacing it with the idempotent script.

```bash
sed -n '1,240p' scripts/routers/router-setup.sh

# Execute only if this script has been reviewed and is safe to rerun:
docker exec -i clab-arista-cer-six-LINUX-PA-01 sh -s -- active < scripts/routers/router-setup.sh
docker exec -i clab-arista-cer-six-LINUX-PA-02 sh -s -- standby < scripts/routers/router-setup.sh
```

## 8. WSL reboot recovery

Symptom: Docker restarts the four Linux nodes, the six cEOS containers are `Exited (255)`, and the Containerlab data-plane veth links are missing.

```bash
cd ~/network-labs/arista-cer
docker ps -a --filter name=clab-arista-cer-six
free -h

# Start the existing switches; keep saved configurations
for sw in MGT-05 MGT-06 MGT-01 MGT-02 MGT-03 MGT-04; do
  docker start "clab-arista-cer-six-$sw"
done

# Check the topology repair plan before any action
sudo containerlab deploy -t cer-ten-node.clab.yml --dry-run

# If ONLY expected link restoration and switch restarts appear:
sudo containerlab deploy -t cer-ten-node.clab.yml
```

Then verify MLAG on the three pairs, restore missing host IP/gateways, restore firewall bond/VLAN/NAT with reviewed scripts, and retest traffic. The six cEOS restarts and 20 link creations were expected during the original recovery. Docker's automatic container restart does **not** ensure the Containerlab data interfaces or Linux runtime setup return.

A locally created `scripts/recover-lab.sh` may automate these steps, but treat it as **unverified until tested successfully**, not as an established WSL boot service.

## 9. Bash commands to memorize

| Command | Meaning |
|---|---|
| `pwd` | Current working directory |
| `cd path` | Change directory |
| `ls -lah` | List files with details |
| `mkdir -p DIR` | Create directory |
| `cp -a SRC DEST` | Copy recursively and preserve metadata |
| `mv SRC DEST` | Move or rename |
| `cat FILE` | Print file |
| `sed -n '1,100p' FILE` | Print lines 1–100 |
| `grep -n PATTERN FILE` | Find text with line numbers |
| `tail -n 50 FILE` | Last 50 lines |
| `less FILE` | Read file interactively |
| `nano FILE` | Edit file |
| `chmod +x FILE` | Make executable |
| `bash -n FILE` / `sh -n FILE` | Syntax check only |
| `./FILE` | Execute script |
| `sudo CMD` | Run as root |
| `echo "$VAR"` | Output variable |
| `$(command)` | Capture command output |
| `A && B` | Run B only if A succeeds |
| `A \| grep WORD` | Filter output |
| `2>&1` | Combine stdout/stderr |
| `Ctrl+C` | Interrupt process |
| `Ctrl+R` | Search command history |
| `history` | Display previous commands |

Example Bash for-loop:

```bash
for sw in MGT-01 MGT-02 MGT-03 MGT-04 MGT-05 MGT-06; do
  docker exec "clab-arista-cer-six-$sw" Cli -p 15 -c 'show mlag'
done
```

## 10. Common failures: first checks

| Symptom | First place to look |
|---|---|
| MLAG `Lowerlayerdown` | Po49; container `eth1/eth2`; `show lacp neighbor` |
| EOS physical interface missing | `docker exec ... ip -br link`; Containerlab topology |
| Host cannot ping gateway | Host `eth1` address, MTU 1500, route, VLAN port |
| Host internet ping succeeds unexpectedly | Route choice may be Docker management bypass |
| Linux firewall `bond0` missing | Was runtime setup rerun after container restart? |
| Internet/NAT broken | IP forwarding, MASQUERADE counters, reverse route |
| cEOS switch stops | `docker inspect` exit/OOM flags; `free -h`; logs |

```bash
free -h
df -h
docker stats --no-stream
docker logs --tail 100 clab-arista-cer-six-MGT-05
docker inspect -f '{{.State.Status}} {{.State.ExitCode}} {{.State.OOMKilled}}' clab-arista-cer-six-MGT-05
```

## 11. Backup and Git essentials

```bash
cd ~/network-labs/arista-cer
STAMP=$(date +%Y%m%d-%H%M%S)
mkdir -p "backup/manual-$STAMP"
cp cer-ten-node.clab.yml "backup/manual-$STAMP/"
cp -a configs scripts "backup/manual-$STAMP/"
chmod -R go-rwx "backup/manual-$STAMP"

git status
git diff
git remote -v
git add docs/
git commit -m 'Document Containerlab lab commands'
# git push  # Only after reviewing changed files
```

Before pushing to a public repository, sanitize configs/logs and never upload secrets, passwords, customer metadata, or generated container state.

## 12. Five-minute self-practice

1. `docker ps -a` — recognize running vs stopped nodes.
2. `show mlag` — identify healthy/failed peer-links.
3. `ip addr show eth1` + `ip route` — understand host forwarding.
4. `cat /proc/net/bonding/bond0` — inspect Linux LACP.
5. `ping -c 4` between hosts and inspect NAT counters.

**Mental model:** Containerlab builds virtual wiring; Docker runs nodes; EOS performs switching/routing; Linux `ip` manages addresses/routes; Linux bonding does LACP; iptables does NAT; Bash automates recovery and testing.
