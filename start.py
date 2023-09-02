import uvicorn
from sys import path as pt
from os import getcwd, path

root_path = getcwd()
pt.append(root_path)

name_app = path.basename(__file__)[0:-3]  # Get the name of the script
log_config = {
"version": 1,
"disable_existing_loggers": True,
"handlers": {
    "file_handler": {
        "class": "logging.FileHandler",
        "filename": "logfile.log",
    },
},
"root": {
    "handlers": ["file_handler"],
    "level": "INFO",
},
}
uvicorn.run(f'canvas_app:app', port=9283, reload=False,log_config=log_config)
