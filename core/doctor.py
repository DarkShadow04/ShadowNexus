import os
import json
import subprocess
import importlib

from rich import print


def check_command(cmd):

    return (
        os.system(
            f"which {cmd} > /dev/null 2>&1"
        ) == 0
    )


def install_package(pkg):

    try:

        subprocess.run(
            [
                "pip",
                "install",
                pkg
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return True

    except:

        return False


def install_termux_package(pkg):

    try:

        subprocess.run(
            [
                "pkg",
                "install",
                "-y",
                pkg
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return True

    except:

        return False


def check_module(module):

    try:

        importlib.import_module(
            module
        )

        return True

    except:

        return False

def quick_health_check():

    try:

        checks = [

            check_command("python"),
            check_command("pip"),

            check_module("rich"),
            check_module("requests"),
            check_module("reportlab"),

            check_command("git"),
            check_command("cloudflared"),
            check_command("neofetch"),

            os.path.exists(
                "config/config.json"
            ),

            os.path.exists(
                "templates"
            ),

            os.path.exists(
                "workspaces"
            ),

            os.path.exists(
                "reports"
            ),

            os.path.exists(
                "server.log"
            )
        ]

        with open(
            "config/config.json",
            "r"
        ) as f:

            cfg = json.load(f)

        root = cfg.get(
            "workspace_root"
        )

        checks.append(
            root
            and
            os.path.exists(root)
        )

        return all(checks)

    except:

        return False


def auto_repair():

    #
    # Python modules
    #

    if not check_module("rich"):
        install_package("rich")

    if not check_module("requests"):
        install_package("requests")

    if not check_module("reportlab"):
        install_package("reportlab")

    #
    # Platform tools
    #

    if not check_command("git"):
        install_termux_package(
            "git"
        )

    if not check_command("cloudflared"):
        install_termux_package(
            "cloudflared"
        )

    if not check_command("neofetch"):
        install_termux_package(
            "neofetch"
        )

    #
    # Workspace structure
    #

    os.makedirs(
        "templates",
        exist_ok=True
    )

    os.makedirs(
        "workspaces",
        exist_ok=True
    )

    os.makedirs(
        "reports",
        exist_ok=True
    )

    if not os.path.exists(
        "server.log"
    ):
        open(
            "server.log",
            "a"
        ).close()


def doctor():

    os.system("clear")

    print()
    print("[bold green]╔══════════════════════════════════════════════════════╗[/bold green]")
    print("[bold green]║                SHADOWNEXUS SYSTEM DOCTOR            ║[/bold green]")
    print("[bold green]╚══════════════════════════════════════════════════════╝[/bold green]")
    print()

    healthy = True

    score = 0
    total = 15

    #
    # SYSTEM COMPONENTS
    #

    print("[bold cyan]SYSTEM COMPONENTS[/bold cyan]")
    print()

    if check_command("python"):

        print("[green][✓][/green] Python")
        score += 1

    else:

        print("[red][✗][/red] Python")
        healthy = False

    if check_command("pip"):

        print("[green][✓][/green] Pip")
        score += 1

    else:

        print("[red][✗][/red] Pip")
        healthy = False

    if check_module("rich"):

        print("[green][✓][/green] Rich")
        score += 1

    else:

        print("[red][✗][/red] Rich - Installing...")

        install_package("rich")

        if check_module("rich"):

            print("    [yellow][FIXED][/yellow]")
            score += 1

        else:

            print("    [red][FAILED][/red]")
            healthy = False

    if check_module("requests"):

        print("[green][✓][/green] Requests")
        score += 1

    else:

        print("[red][✗][/red] Requests - Installing...")

        install_package("requests")

        if check_module("requests"):

            print("    [yellow][FIXED][/yellow]")
            score += 1

        else:

            print("    [red][FAILED][/red]")
            healthy = False

    if check_module("reportlab"):

        print("[green][✓][/green] ReportLab")
        score += 1

    else:

        print("[red][✗][/red] ReportLab - Installing...")

        install_package("reportlab")

        if check_module("reportlab"):

            print("    [yellow][FIXED][/yellow]")
            score += 1

        else:

            print("    [red][FAILED][/red]")
            healthy = False

    print()
    print("[green]" + "═" * 54 + "[/green]")
    print()

    #
    # PLATFORM COMPONENTS
    #

    print("[bold cyan]PLATFORM COMPONENTS[/bold cyan]")
    print()

    if check_command("git"):

        print("[green][✓][/green] Git")
        score += 1

    else:

        print("[red][✗][/red] Git")
        healthy = False

    if check_command("cloudflared"):

        print("[green][✓][/green] Cloudflared")
        score += 1

    else:

        print("[red][✗][/red] Cloudflared")
        healthy = False

    if check_command("neofetch"):

        print("[green][✓][/green] Neofetch")
        score += 1

    else:

        print("[red][✗][/red] Neofetch - Installing...")

        install_termux_package(
            "neofetch"
        )

        if check_command("neofetch"):

            print("    [yellow][FIXED][/yellow]")
            score += 1

        else:

            print("    [red][FAILED][/red]")
            healthy = False

    print()
    print("[green]" + "═" * 54 + "[/green]")
    print()

    #
    # WORKSPACE COMPONENTS
    #

    print("[bold cyan]WORKSPACE COMPONENTS[/bold cyan]")
    print()

    if os.path.exists(
        "config/config.json"
    ):

        print("[green][✓][/green] Config")
        score += 1

    else:

        print("[red][✗][/red] Config Missing")
        healthy = False

    if os.path.exists("templates"):

        print("[green][✓][/green] Templates Folder")
        score += 1

    else:

        os.makedirs(
            "templates",
            exist_ok=True
        )

        print("[red][✗][/red] Templates Missing")
        print("    [yellow][FIXED][/yellow]")
        score += 1

    if os.path.exists("workspaces"):

        print("[green][✓][/green] Workspaces Folder")
        score += 1

    else:

        os.makedirs(
            "workspaces",
            exist_ok=True
        )

        print("[red][✗][/red] Workspaces Missing")
        print("    [yellow][FIXED][/yellow]")
        score += 1

    if os.path.exists("reports"):

        print("[green][✓][/green] Reports Folder")
        score += 1

    else:

        os.makedirs(
            "reports",
            exist_ok=True
        )

        print("[red][✗][/red] Reports Missing")
        print("    [yellow][FIXED][/yellow]")
        score += 1

    if os.path.exists("server.log"):

        print("[green][✓][/green] Server Log")
        score += 1

    else:

        open(
            "server.log",
            "a"
        ).close()

        print("[red][✗][/red] Server Log Missing")
        print("    [yellow][FIXED][/yellow]")
        score += 1

    print()
    print("[green]" + "═" * 54 + "[/green]")
    print()

    #
    # SECURITY COMPONENTS
    #

    print("[bold cyan]SECURITY COMPONENTS[/bold cyan]")
    print()

    try:

        with open(
            "config/config.json",
            "r"
        ) as f:

            cfg = json.load(f)

        print("[green][✓][/green] Config Integrity")
        score += 1

    except:

        print("[red][✗][/red] Config Integrity")
        healthy = False

    try:

        root = cfg.get(
            "workspace_root"
        )

        if (
            root
            and os.path.exists(root)
        ):

            print("[green][✓][/green] Workspace Root")
            score += 1

        else:

            print("[red][✗][/red] Workspace Root")
            healthy = False

    except:

        print("[red][✗][/red] Workspace Root")
        healthy = False

    print()
    print("[green]" + "═" * 54 + "[/green]")
    print()

    #
    # SUMMARY
    #

    percentage = round(
        (score / total) * 100
    )

    print("[bold cyan]SYSTEM SUMMARY[/bold cyan]")
    print()

    print(
        f"[green]SYSTEM SCORE[/green]  : {percentage}%"
    )

    if healthy:

        print(
            "[green]SYSTEM STATUS[/green] : HEALTHY"
        )

    else:

        print(
            "[red]SYSTEM STATUS[/red] : NEEDS ATTENTION"
        )

    print()
    print("[green]" + "═" * 54 + "[/green]")

    input(
        "\nPress Enter to continue..."
    )