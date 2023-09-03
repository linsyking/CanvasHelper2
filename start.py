#!/usr/bin/env python3

import uvicorn
from canvas_app import app

"""
Start script
"""


if __name__ == "__main__":
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
            "level": "INFO",
        },
    }

    uvicorn.run(app, port=9283, reload=False, log_config=log_config)
