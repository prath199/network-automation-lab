"""SSH transport: strict SSH keys, bounded timeouts and read-only commands."""
import os
from netmiko import ConnectHandler
from .common import auth_env

def show(device, command):
    if not command.lstrip().startswith("show "):
        raise ValueError("Read-only show commands only")
    with ConnectHandler(device_type=device["platform"], host=device["host"],
                        username=os.environ["NETOPS_USERNAME"],
                        password=auth_env(device), conn_timeout=10,
                        auth_timeout=10, banner_timeout=15,
                        timeout=20, fast_cli=False,
                        ssh_strict=True, system_host_keys=True,
                        alt_host_keys=False) as session:
        return session.send_command(command, read_timeout=30)

