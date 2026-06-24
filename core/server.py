import os
import json
import signal
import socket
import subprocess
import threading
from datetime import datetime
import re
from collections import Counter

from rich import print
from core.config import (
    load_config,
    save_config
)

SERVER_FILE = "config/server.json"
LOG_FILE = "server.log"


def get_local_ip():

    try:

        s = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

        s.connect(("8.8.8.8", 80))

        ip = s.getsockname()[0]

        s.close()

        return ip

    except:

        return "127.0.0.1"


def save_server(data):

    os.makedirs("config", exist_ok=True)

    with open(SERVER_FILE, "w") as f:

        json.dump(
            data,
            f,
            indent=4
        )


def load_server():

    if not os.path.exists(SERVER_FILE):
        return None

    try:

        with open(SERVER_FILE) as f:
            return json.load(f)

    except:
        return None


def is_running(pid):

    try:

        os.kill(pid, 0)
        return True

    except:

        return False

def tunnel_logger(pipe):

    try:

        with open(
            LOG_FILE,
            "a"
        ) as log:

            while True:

                line = pipe.readline()

                if not line:
                    break

                log.write(
                    "[TUNNEL] "
                    + line
                )

                log.flush()

    except:

        pass


def start_server():

    cfg = load_config()

    path = cfg.get(
        "workspace_root",
        ""
    )

    change = input(
        f"Use saved path? [{path}] (Y/n): "
    ).lower().strip()

    if change == "n" or not path:

        path = input(
            "Website Path: "
        ).strip()

        cfg["workspace_root"] = path

        save_config(cfg)

    port = input(
        "Port [8080]: "
    ).strip() or "8080"

    try:

        log_file = open(
            LOG_FILE,
            "a"
        )

        process = subprocess.Popen(
            [
                "python",
                "-m",
                "http.server",
                port
            ],
            cwd=path,
            stdout=log_file,
            stderr=log_file
        )

        save_server(
            {
                "pid": process.pid,
                "port": port,
                "path": path,
                "started": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            }
        )

        print()
        print("[green] SERVER STARTED[/green]")
        print()

        print(f"PID   : {process.pid}")
        print(f"PORT  : {port}")
        print(
            f"URL   : http://{get_local_ip()}:{port}"
        )

    except Exception as e:

        print(f"[red]{e}[/red]")

    input("\nPress Enter...")


def stop_server():

    server = load_server()

    if not server:

        print("[red]No server running.[/red]")
        input("\nPress Enter...")
        return

    try:

        os.kill(
            server["pid"],
            signal.SIGTERM
        )

    except:
        pass

    if os.path.exists(SERVER_FILE):
        os.remove(SERVER_FILE)

    print()
    print("[green] SERVER STOPPED[/green]")

    input("\nPress Enter...")

def start_public_tunnel():

    server = load_server()

    if not server:

        print()
        print(
            "[red]Start local server first.[/red]"
        )

        input("\nPress Enter...")
        return

    if server.get("public_url"):

        print()
        print(
            "[yellow]Tunnel already running.[/yellow]"
        )

        print(
            server["public_url"]
        )

        input("\nPress Enter...")
        return

    try:

        process = subprocess.Popen(
            [
                "cloudflared",
                "tunnel",
                "--url",
                f"http://localhost:{server['port']}"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        public_url = None

        while True:

            line = process.stdout.readline()

            if not line:
                continue

            match = re.search(
                r"https://[a-zA-Z0-9\-]+\.trycloudflare\.com",
                line
            )

            if match:

                public_url = (
                    match.group(0)
                )

                break

        threading.Thread(
            target=tunnel_logger,
            args=(process.stdout,),
            daemon=True
        ).start()

        server["tunnel_pid"] = (
            process.pid
        )

        server["public_url"] = (
            public_url
        )

        server["tunnel_started"] = (
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        save_server(server)

        print()
        print(
            "[green]✓ PUBLIC TUNNEL STARTED[/green]"
        )

        print()
        print(
            f"PUBLIC URL : {public_url}"
        )

    except Exception as e:

        print()
        print(
            f"[red]{e}[/red]"
        )

    input("\nPress Enter...")

def stop_public_tunnel():

    server = load_server()

    if not server:
        return

    pid = server.get(
        "tunnel_pid"
    )

    if not pid:

        print()
        print(
            "[yellow]No tunnel running.[/yellow]"
        )

        input("\nPress Enter...")
        return

    try:

        os.kill(
            int(pid),
            signal.SIGTERM
        )

    except:
        pass

    server.pop(
        "tunnel_pid",
        None
    )

    server.pop(
        "public_url",
        None
    )

    server.pop(
        "tunnel_started",
        None
    )

    save_server(server)

    print()
    print(
        "[green]✓ PUBLIC TUNNEL STOPPED[/green]"
    )

    input("\nPress Enter...")


def tunnel_info():

    server = load_server()

    if not server:

        print(
            "[red]No server running.[/red]"
        )

        input("\nPress Enter...")
        return

    os.system("clear")

    print()
    print(
        "[bold green]PUBLIC TUNNEL[/bold green]"
    )

    print()

    print(
        f"URL     : {server.get('public_url','---')}"
    )

    print(
        f"PID     : {server.get('tunnel_pid','---')}"
    )

    print(
        f"STARTED : {server.get('tunnel_started','---')}"
    )

    print()

    input(
        "Press Enter..."
    )

def restart_server():

    stop_server()
    start_server()



def server_info():

    server = load_server()

    if not server:

        print("[red]No server data.[/red]")
        input("\nPress Enter...")
        return

    print()
    print("[bold green]SERVER INFORMATION[/bold green]")
    print()

    print(f"PID     : {server['pid']}")
    print(f"PORT    : {server['port']}")
    print(f"PATH    : {server['path']}")
    print(f"STARTED : {server['started']}")

    print(
        f"URL     : http://{get_local_ip()}:{server['port']}"
    )

    if server.get("public_url"):

        print(
            f"PUBLIC  : {server['public_url']}"
        )

    input("\nPress Enter...")

def website_analytics():

    server = load_server()

    if not server:

        print("[red]No server running.[/red]")
        input("\nPress Enter...")
        return

    path = server["path"]

    files_count = 0
    folders_count = 0

    html_count = 0
    css_count = 0
    js_count = 0
    image_count = 0

    total_size = 0

    image_ext = (
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".webp",
        ".svg",
        ".bmp",
        ".ico"
    )

    for root, dirs, files in os.walk(path):

        folders_count += len(dirs)

        for file in files:

            files_count += 1

            full_path = os.path.join(
                root,
                file
            )

            try:
                total_size += os.path.getsize(
                    full_path
                )
            except:
                pass

            lower = file.lower()

            if lower.endswith(
                (".html", ".htm")
            ):
                html_count += 1

            elif lower.endswith(".css"):
                css_count += 1

            elif lower.endswith(".js"):
                js_count += 1

            elif lower.endswith(image_ext):
                image_count += 1

    size_mb = round(
        total_size / (1024 * 1024),
        2
    )

    total_visits = 0
    unique_ips = set()

    status_200 = 0
    status_304 = 0
    status_404 = 0

    pages = Counter()

    last_ip = "---"
    last_page = "---"
    last_time = "---"

    try:

        if os.path.exists(LOG_FILE):

            with open(
                LOG_FILE,
                "r",
                errors="ignore"
            ) as f:

                lines = f.readlines()

            for line in lines:

                if "GET " not in line:
                    continue

                total_visits += 1

                ip_match = re.search(
                    r'([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)',
                    line
                )

                if ip_match:

                    ip = ip_match.group(1)

                    unique_ips.add(ip)

                    last_ip = ip

                page_match = re.search(
                    r'"GET (.*?) HTTP',
                    line
                )

                if page_match:

                    page = page_match.group(1)

                    pages[page] += 1

                    last_page = page

                time_match = re.search(
                    r'\[(.*?)\]',
                    line
                )

                if time_match:

                    last_time = time_match.group(1)

                if '" 200 ' in line:
                    status_200 += 1

                elif '" 304 ' in line:
                    status_304 += 1

                elif '" 404 ' in line:
                    status_404 += 1

    except:
        pass

    success_total = (
        status_200 +
        status_304 +
        status_404
    )

    if success_total:

        success_rate = round(
            (
                (
                    status_200 +
                    status_304
                ) /
                success_total
            ) * 100,
            1
        )

    else:

        success_rate = 0

    top_pages = pages.most_common(3)

    os.system("clear")

    print()
    print("[bold green]WEBSITE ANALYTICS[/bold green]")
    print()

    print(f"ROOT : {path}")
    print()

    print(f"[green][][/green] FILES        : {files_count}")
    print(f"[green][][/green] HTML         : {html_count}")
    print(f"[green][][/green] CSS          : {css_count}")
    print(f"[green][][/green] JS           : {js_count}")
    print(f"[green][][/green] IMAGES       : {image_count}")
    print(f"[green][][/green] FOLDERS      : {folders_count}")
    print(f"[green][][/green] TOTAL SIZE   : {size_mb} MB")

    print()
    print("=" * 40)
    print()

    print(f"TOTAL VISITS    : {total_visits}")
    print(f"UNIQUE VISITORS : {len(unique_ips)}")

    print()
    print("=" * 40)
    print()

    print("HTTP STATUS")
    print()

    print(f"200 OK      : {status_200}")
    print(f"304 CACHE   : {status_304}")
    print(f"404 ERRORS  : {status_404}")

    print()
    print(f"SUCCESS RATE : {success_rate}%")

    print()
    print("=" * 40)
    print()

    print("MOST VISITED")
    print()

    if top_pages:

        for page, count in top_pages:

            print(
                f"{page:<20} {count}"
            )

    else:

        print("No data")

    print()
    print("=" * 40)
    print()

    print("LAST VISITOR")
    print()

    print(f"IP    : {last_ip}")
    print(f"TIME  : {last_time}")
    print(f"PAGE  : {last_page}")

    print()
    print("=" * 40)
    print()

    input("\nPress Enter...")

def website_structure():

    server = load_server()

    if not server:

        print("[red]No server running.[/red]")
        input("\nPress Enter...")
        return

    os.system("clear")

    print()
    print("[bold green]WEBSITE STRUCTURE[/bold green]")
    print()

    print(f"ROOT : {server['path']}")
    print()

    tree(server["path"])

    input("\nPress Enter...")


def live_logs():

    server = load_server()

    if not server:

        print("[red]No server running.[/red]")
        input("\nPress Enter...")
        return

    while True:

        os.system("clear")

        print()
        print(
            "[bold green]SERVER LOGS[/bold green]"
        )
        print()

        print(
            f"PATH : {server['path']}"
        )

        print(
            f"URL  : http://{get_local_ip()}:{server['port']}"
        )

        if server.get("public_url"):

            print(
                f"PUBLIC URL : {server['public_url']}"
            )

        print()
        print("=" * 60)
        print("LATEST LOG ENTRIES")
        print("=" * 60)
        print()

        if os.path.exists(LOG_FILE):

            try:

                with open(
                    LOG_FILE,
                    "r",
                    errors="ignore"
                ) as f:

                    lines = f.readlines()

                for line in lines[-20:]:

                    print(
                        line.rstrip()
                    )

            except Exception as e:

                print(
                    f"[red]{e}[/red]"
                )

        else:

            print(
                "[yellow]No log file found.[/yellow]"
            )

        print()
        print("=" * 60)
        print("[R] Refresh")
        print("[Q] Back")
        print("=" * 60)

        choice = input(
            "\nLogs > "
        ).lower().strip()

        if choice == "q":

            break

def tree(path, prefix=""):

    try:

        items = sorted(
            os.listdir(path)
        )

    except:

        return

    for i, item in enumerate(items):

        full = os.path.join(
            path,
            item
        )

        last = (
            i == len(items) - 1
        )

        connector = (
            "└── "
            if last
            else "├── "
        )

        print(
            prefix + connector + item
        )

        if os.path.isdir(full):

            extension = (
                "    "
                if last
                else "│   "
            )

            tree(
                full,
                prefix + extension
            )

def server_menu():

    while True:

        os.system("clear")

        print()
        print("[bold green]SERVER MANAGER[/bold green]")
        print()

        print("[1] Start Server")
        print("[2] Stop Server")
        print("[3] Restart Server")
        print("[4] Server Information")
        print("[5] Website Analytics")
        print("[6] Website Structure")
        print("[7] Live Logs")

        print()

        print("[8] Start Public Tunnel")
        print("[9] Stop Public Tunnel")
        print("[A] Tunnel Information")

        print()
        print("[X] Back")
        print()

        choice = input(
            "Server > "
        ).lower().strip()

        if choice == "1":

            start_server()

        elif choice == "2":

            stop_server()

        elif choice == "3":

            restart_server()

        elif choice == "4":

            server_info()

        elif choice == "5":

            website_analytics()

        elif choice == "6":

            website_structure()

        elif choice == "7":

            live_logs()

        elif choice == "8":

            start_public_tunnel()

        elif choice == "9":

            stop_public_tunnel()

        elif choice == "a":

            tunnel_info()

        elif choice == "x":

            break