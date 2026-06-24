import json
import os
import re
import subprocess

from core.doctor import (
    quick_health_check
)

from datetime import datetime
from rich import print

from core.config import load_config

SERVER_FILE = "config/server.json"


def run(cmd):
    try:
        return subprocess.check_output(
            cmd,
            shell=True,
            stderr=subprocess.DEVNULL
        ).decode("utf-8")
    except:
        return ""


def neofetch_value(key):

    data = run("neofetch --stdout")

    for line in data.splitlines():

        if line.startswith(key):
            return line.split(":", 1)[1].strip()

    return "N/A"


def get_local_ip():

    data = run("ifconfig")

    matches = re.findall(
        r"inet\s+(\d+\.\d+\.\d+\.\d+)",
        data
    )

    for ip in matches:

        if (
            ip != "127.0.0.1"
            and not ip.startswith("169.254.")
        ):
            return ip

    return None


def get_server():

    if not os.path.exists(SERVER_FILE):
        return None

    try:

        with open(SERVER_FILE, "r") as f:
            return json.load(f)

    except:
        return None


def is_server_running():

    server = get_server()

    if not server:
        return False

    pid = server.get("pid")

    if not pid:
        return False

    result = run(f"ps -A | grep {pid}")

    return str(pid) in result


def server_uptime():

    server = get_server()

    if not server:
        return "---"

    try:

        started = datetime.strptime(
            server["started"],
            "%Y-%m-%d %H:%M:%S"
        )

        diff = datetime.now() - started

        total = int(diff.total_seconds())

        hours = total // 3600
        minutes = (total % 3600) // 60
        seconds = total % 60

        return f"{hours:02}:{minutes:02}:{seconds:02}"

    except:
        return "---"


def dashboard():

    cfg = load_config()

    server = get_server()

    security_ok = quick_health_check()

    local_ip = get_local_ip()

    network_online = local_ip is not None

    process_running = is_server_running()

    if network_online:

        online = process_running

    else:

        online = False

    pid = "---"
    port = "---"
    url = "---"

    if server:

        pid = server.get(
            "pid",
            "---"
        )

        port = server.get(
            "port",
            "---"
        )

        if online and local_ip:

            url = (
                f"http://{local_ip}:{port}"
            )

    public_url = "---"

    tunnel_status = "[red]OFFLINE[/red]"

    if network_online and server:

        public_url = server.get(
            "public_url",
            "---"
        )

        if (
            public_url
            and public_url != "---"
        ):

            tunnel_status = (
                "[green]ONLINE[/green]"
            )

    os.system("clear")

    now = datetime.now()

    print()
    print("[bold green]╔══════════════════════════════════════════════════════╗[/bold green]")
    print("[bold green]║                SHADOWNEXUS CONTROL MATRIX           ║[/bold green]")
    print("[bold green]╚══════════════════════════════════════════════════════╝[/bold green]")
    print()

    print("[green][✔][/green] SYSTEM ONLINE")

    if network_online:

        print(
            "[green][✔][/green] NETWORK ACTIVE"
        )

    else:

        print(
            "[red][✘][/red] NETWORK OFFLINE"
        )

    if security_ok:

        print(
            "[green][✔][/green] SECURITY HEALTHY"
        )

    else:

        print(
            "[red][✘][/red] SECURITY ISSUES"
        )

    print(
        "[green][✔][/green] WORKSPACE MOUNTED"
    )

    if online:

        print(
            "[green][✔][/green] SERVER ONLINE"
        )

    else:

        print(
            "[red][✘][/red] SERVER OFFLINE"
        )

    print()

    print(
        "[green]" + "═" * 54 + "[/green]"
    )

    print(
        f"[cyan]DATE[/cyan]      {now.strftime('%d-%m-%Y')}"
    )

    print(
        f"[cyan]TIME[/cyan]      {now.strftime('%H:%M:%S')}"
    )

    print(
        "[green]" + "═" * 54 + "[/green]"
    )

    print(
        f"[green]OS[/green]         {neofetch_value('OS')}"
    )

    print(
        f"[green]HOST[/green]       {neofetch_value('Host')}"
    )

    print(
        f"[green]KERNEL[/green]     {neofetch_value('Kernel')}"
    )

    print(
        f"[green]UPTIME[/green]     {neofetch_value('Uptime')}"
    )

    print(
        f"[green]PACKAGES[/green]   {neofetch_value('Packages')}"
    )

    print(
        f"[green]SHELL[/green]      {neofetch_value('Shell')}"
    )

    print(
        f"[green]CPU[/green]        {neofetch_value('CPU')}"
    )

    print(
        f"[green]MEMORY[/green]     {neofetch_value('Memory')}"
    )

    print(
        "[green]" + "═" * 54 + "[/green]"
    )

    if local_ip:

        print(
            f"[cyan]LOCAL IP[/cyan]   {local_ip}"
        )

    else:

        print(
            "[cyan]LOCAL IP[/cyan]   ---"
        )

    print(
        f"[cyan]WORKSPACE[/cyan]  {cfg['workspace']}"
    )

    print(
        f"[cyan]THEME[/cyan]      {cfg['theme']}"
    )

    print(
        "[green]" + "═" * 54 + "[/green]"
    )

    print(
        f"[magenta]PID[/magenta]        {pid}"
    )

    print(
        f"[magenta]PORT[/magenta]       {port}"
    )

    print(
        f"[magenta]UPTIME[/magenta]     {server_uptime()}"
    )

    if online:

        print(
            "[magenta]STATUS[/magenta]     [green]ONLINE[/green]"
        )

    else:

        print(
            "[magenta]STATUS[/magenta]     [red]OFFLINE[/red]"
        )

    print(
        f"[magenta]PUBLIC URL[/magenta] {public_url}"
    )

    print(
        f"[magenta]LOCAL URL[/magenta]  {url}"
    )

    print(
        f"[magenta]TUNNEL[/magenta]     {tunnel_status}"
    )

    print(
        "[green]" + "═" * 54 + "[/green]"
    )