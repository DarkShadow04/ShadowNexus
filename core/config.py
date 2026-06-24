import json
import os

DEFAULT_CONFIG = {
    "workspace": "",
    "workspace_root": "",
    "theme": "shadow"
}


def load_config():

    os.makedirs(
        "config",
        exist_ok=True
    )

    if not os.path.exists(
        "config/config.json"
    ):

        save_config(
            DEFAULT_CONFIG
        )

        return DEFAULT_CONFIG

    try:

        with open(
            "config/config.json",
            "r"
        ) as f:

            data = json.load(f)

        changed = False

        for key, value in DEFAULT_CONFIG.items():

            if key not in data:

                data[key] = value
                changed = True

        if changed:

            save_config(data)

        return data

    except:

        save_config(
            DEFAULT_CONFIG
        )

        return DEFAULT_CONFIG


def save_config(data):

    os.makedirs(
        "config",
        exist_ok=True
    )

    with open(
        "config/config.json",
        "w"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )