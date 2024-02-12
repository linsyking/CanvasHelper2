#!/usr/bin/env python3

import uvicorn
from canvas_app import app
import json
from os import path

"""
Start script
"""


if __name__ == "__main__":
    net_config = {}

    log_config = {
        "version": 1,
        "disable_existing_loggers": True,
        "handlers": {
            "file_handler": {
                "class": "logging.FileHandler",
                "filename": "error.log",
            },
        },
        "root": {
            "handlers": ["file_handler"],
            "level": "ERROR",
        },
    }

    if path.exists("net_config.json"):
        with open("net_config.json", "r", encoding="utf-8", errors="ignore") as f:
            net_config = json.load(f)

            if "host" not in net_config:
                raise Exception("no host")
            elif "port" not in net_config:
                raise Exception("no port")

            usr_host = net_config["host"]
            usr_port = net_config["port"]
    else:
        usr_host = "localhost"
        usr_port = 9283

    uvicorn.run(app, port=usr_port, host=usr_host, reload=False, log_config=log_config)
