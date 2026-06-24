import os
import json

from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

LOG_FILE = "server.log"
SERVER_FILE = "config/server.json"
CONFIG_FILE = "config/config.json"


def create_reports_folder():

    now = datetime.now()

    year = now.strftime("%Y")
    month = now.strftime("%m")

    folder = os.path.join(
        "reports",
        year,
        month
    )

    os.makedirs(
        folder,
        exist_ok=True
    )

    return folder


def create_report_filename():

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    return f"Session_{timestamp}.pdf"


def load_server():

    try:

        with open(
            SERVER_FILE,
            "r"
        ) as f:

            return json.load(f)

    except:

        return {}


def load_config():

    try:

        with open(
            CONFIG_FILE,
            "r"
        ) as f:

            return json.load(f)

    except:

        return {}


def load_logs():

    if not os.path.exists(
        LOG_FILE
    ):
        return ""

    try:

        with open(
            LOG_FILE,
            "r"
        ) as f:

            return f.read()

    except:

        return ""


def clear_logs():

    open(
        LOG_FILE,
        "w"
    ).close()


def count_requests(logs):

    stats = {
        "200": 0,
        "304": 0,
        "404": 0,
        "500": 0
    }

    for line in logs.splitlines():

        if " 200 " in line:
            stats["200"] += 1

        elif " 304 " in line:
            stats["304"] += 1

        elif " 404 " in line:
            stats["404"] += 1

        elif " 500 " in line:
            stats["500"] += 1

    return stats


def generate_session_report():

    folder = create_reports_folder()

    filename = create_report_filename()

    pdf_path = os.path.join(
        folder,
        filename
    )

    config = load_config()

    server = load_server()

    logs = load_logs()

    stats = count_requests(
        logs
    )

    now = datetime.now()

    session_id = now.strftime(
        "SNX-%Y%m%d-%H%M%S"
    )

    doc = SimpleDocTemplate(
        pdf_path
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "SHADOWNEXUS SESSION REPORT",
            styles["Title"]
        )
    )

    content.append(
        Paragraph(
            f"Session ID: {session_id}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            "Generated: "
            + now.strftime(
                "%d-%b-%Y %H:%M:%S"
            ),
            styles["Normal"]
        )
    )

    content.append(
        Spacer(
            1,
            20
        )
    )

    content.append(
        Paragraph(
            "WORKSPACE DETAILS",
            styles["Heading1"]
        )
    )

    content.append(
        Paragraph(
            f"Workspace: {config.get('workspace', 'Unknown')}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Theme: {config.get('theme', 'Unknown')}",
            styles["Normal"]
        )
    )

    content.append(
        Spacer(
            1,
            20
        )
    )

    content.append(
        Paragraph(
            "SERVER DETAILS",
            styles["Heading1"]
        )
    )

    content.append(
        Paragraph(
            f"PID: {server.get('pid', '---')}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"PORT: {server.get('port', '---')}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"URL: {server.get('url', '---')}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"STARTED: {server.get('started', '---')}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"ENDED: {now.strftime('%d-%b-%Y %H:%M:%S')}",
            styles["Normal"]
        )
    )

    content.append(
        Spacer(
            1,
            20
        )
    )

    content.append(
        Paragraph(
            "REQUEST STATISTICS",
            styles["Heading1"]
        )
    )

    content.append(
        Paragraph(
            f"200 OK : {stats['200']}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"304 Cached : {stats['304']}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"404 Not Found : {stats['404']}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"500 Errors : {stats['500']}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Total Log Entries : {len(logs.splitlines())}",
            styles["Normal"]
        )
    )

    content.append(
        Spacer(
            1,
            20
        )
    )

    content.append(
        PageBreak()
    )

    content.append(
        Paragraph(
            "RAW SERVER LOGS",
            styles["Heading1"]
        )
    )

    if logs.strip():

        for line in logs.splitlines():

            safe_line = (
                line.replace(
                    "&",
                    "&amp;"
                )
                .replace(
                    "<",
                    "&lt;"
                )
                .replace(
                    ">",
                    "&gt;"
                )
            )

            content.append(
                Paragraph(
                    safe_line,
                    styles["Normal"]
                )
            )

    else:

        content.append(
            Paragraph(
                "No log entries found.",
                styles["Normal"]
            )
        )

    content.append(
        Spacer(
            1,
            20
        )
    )

    content.append(
        Paragraph(
            "Generated by ShadowNexus",
            styles["Italic"]
        )
    )

    content.append(
        Paragraph(
            "Copyright © Dark_Shadow04",
            styles["Italic"]
        )
    )

    doc.build(
        content
    )

    clear_logs()

    return pdf_path