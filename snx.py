import os

from rich.console import Console

from core.archive import generate_session_report
from core.dashboard import dashboard
from core.workspace import workspace_manager
from core.server import (
    server_menu,
    stop_server,
    stop_public_tunnel,
    load_server
)
from core.doctor import (
    doctor,
    auto_repair
)
from core.templates import template_manager

console = Console()


def shutdown_shadow_nexus():

    print()

    archive = input(
        "Archive session report? [Y/N] > "
    ).lower().strip()

    if archive == "y":

        try:

            report = generate_session_report()

            print()
            print("[] Session archived")
            print(report)

        except Exception as e:

            print()
            print(
                f"[] Archive failed: {e}"
            )

    print()

    server = load_server()

    if (
        server
        and server.get("tunnel_pid")
        and server.get("public_url")
    ):

        keep_tunnel = input(
            "Keep public tunnel running? [Y/N] > "
        ).lower().strip()

        if keep_tunnel == "n":

            try:

                stop_public_tunnel()

                print(
                    "[] Public tunnel stopped"
                )

            except Exception as e:

                print(
                    f"[] Tunnel stop failed: {e}"
                )

        else:

            print(
                "[] Public tunnel left running"
            )

        print()

    keep_server = input(
        "Keep local server running? [Y/N] > "
    ).lower().strip()

    if keep_server == "n":

        try:

            stop_server()

            print(
                "[] Server stopped"
            )

        except:

            print(
                "[!] No active server"
            )

    else:

        print(
            "[] Server left running"
        )

    print()
    print("[] Session closed")
    print()
    print("Goodbye.")
    print("See you later.")
    print()
    print("Copyright (C) Dark_Shadow04")


    raise SystemExit

#
# Startup Health Check
#

try:

    auto_repair()

except:

    pass


while True:

    os.system("clear")

    dashboard()

    print("""
[1] Workspace Manager
[2] Server Manager
[3] System Doctor
[4] Templates

[X] Exit
""")

    choice = input(
        "ShadowNexus > "
    ).lower().strip()

    if choice == "1":

        workspace_manager()

    elif choice == "2":

        server_menu()

    elif choice == "3":

        doctor()

    elif choice == "4":

        template_manager()

    elif choice == "x":

        shutdown_shadow_nexus()

    else:

        input(
            "\nInvalid option..."
        )