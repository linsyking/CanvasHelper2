#!/usr/bin/env python3

from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from config_mgr import ConfigMGR
from canvas_mgr import CanvasMGR
import urllib.parse
from models import Position, Check, Course, URL
from fastapi.responses import JSONResponse
from os import path, listdir, remove, mkdir, getcwd
from updater import update
import json
import logging
from typing import List
import uvicorn
from sys import path as pt

root_path = getcwd()
pt.append(root_path)

"""
Local function
"""

ALLOWED_EXTENSION = {
    "png",
    "jpg",
    "jpeg",
    "gif",
    "svg",
    "mp4",
    "mkv",
    "mov",
    "m4v",
    "avi",
    "wmv",
    "webm",
}


# INFO: Safety check for file
def check_file(filename):
    base_path = "/public/res/"
    fullPath = path.normpath(path.join(base_path, filename))
    if (
        not "." in filename
        or not filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSION
    ):
        return "Illegal"
    if not fullPath.startswith(base_path):
        return "Illegal"
    else:
        return filename


"""
Canvas App

This file contains all the APIs to access the
configuration file/canvas backend, etc..
"""


app = FastAPI(version="1.0.1", title="Canvas Helper", description="Canvas Helper API.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

conf = ConfigMGR()

# Self Update
update()


@app.get(
    "/config",
    summary="Get the configuration file",
    description="Get the configuration file.",
    tags=["config"],
)
async def get_configuration():
    return conf.get_conf()


@app.get(
    "/config/refresh",
    tags=["config"],
    summary="Refresh the configuration file",
    description="Force to read the configuration file from disk.",
)
async def refresh_conf():
    conf.force_read()
    return JSONResponse(status_code=200, content={"message": "success"})


@app.get(
    "/config/key/{key}",
    tags=["config"],
    summary="Get a specific key from the configuration file",
    description="Get a specific key from the configuration file.",
)
async def get_configuration_key(key: str):
    if key not in conf.get_conf():
        return JSONResponse(status_code=404, content={"message": "Key not found"})
    return conf.get_conf()[key]


@app.put(
    "/config/key/{key}",
    tags=["config"],
    summary="Update a specific key in the configuration file",
    description="Update a specific key in the configuration file.",
)
async def update_configuration(key: str, request: Request):
    body = await request.body()
    try:
        body_p = json.loads('{"data" : ' + body.decode(encoding="utf-8") + "}")
    except:
        return JSONResponse(status_code=400, content={"message": "Cannot parse body"})
    conf.set_key_value(key, body_p["data"])
    return JSONResponse(status_code=200, content={"message": "success"})


@app.delete(
    "/config/key/{key}",
    tags=["config"],
    summary="Delete a specific key in the configuration file",
    description="Delete a specific key in the configuration file.",
)
async def delete_configuration(key: str):
    if key not in conf.get_conf():
        return JSONResponse(status_code=404, content={"message": "Key not found"})
    conf.remove_key(key)
    return JSONResponse(status_code=200, content={"message": "success"})


@app.get(
    "/config/verify",
    tags=["config"],
    summary="Verify the configuration file",
    description="Verify the configuration file.",
)
async def verify_config():
    """
    Verify the configuration
    """
    if "bid" not in conf.get_conf():
        return JSONResponse(status_code=404, content={"message": "bid not found"})
    if "url" not in conf.get_conf():
        return JSONResponse(status_code=404, content={"message": "url not found"})
    if "background_image" not in conf.get_conf() and "video" not in conf.get_conf():
        return JSONResponse(status_code=400, content={"message": "background not set"})
    # Test bid

    import requests

    headers = {"Authorization": f'Bearer {conf.get_conf()["bid"]}'}
    url = str(conf.get_conf()["url"])
    if url.find("http://") != 0 and url.find("https://") != 0:
        # Invalid protocal
        url = "https://" + url
        conf.set_key_value("url", url)
    res = requests.get(
        urllib.parse.urljoin(url, "api/v1/accounts"), headers=headers
    ).status_code
    if res == 200:
        return JSONResponse(status_code=200, content={"message": "success"})
    else:
        return JSONResponse(status_code=400, content={"message": "verification failed"})


@app.get(
    "/courses",
    tags=["course"],
    summary="Get all the courses",
    description="Get all the courses.",
)
async def get_all_courses():
    if "courses" not in conf.get_conf():
        return []
    return conf.get_conf()["courses"]


@app.get(
    "/courses/canvas",
    tags=["course"],
    summary="Get all the courses from canvas",
    description="Get all the courses from canvas.",
)
async def get_all_canvas_courses():
    if "bid" not in conf.get_conf():
        return JSONResponse(status_code=404, content={"message": "bid not found"})

    import requests

    headers = {"Authorization": f'Bearer {conf.get_conf()["bid"]}'}
    res = requests.get(
        urllib.parse.urljoin(
            str(conf.get_conf()["url"]), "api/v1/dashboard/dashboard_cards"
        ),
        headers=headers,
    ).text
    return json.loads(res)


@app.delete(
    "/courses/{course_id}",
    tags=["course"],
    summary="Delete a course",
    description="Delete a course. It will delete all the course items with the given course id.",
)
async def delete_course(course_id: int):
    if "courses" not in conf.get_conf():
        return JSONResponse(status_code=404, content={"message": "Courses not found"})
    courses = conf.get_conf()["courses"]
    all_courses = []
    if not isinstance(courses, List):
        return JSONResponse(
            status_code=404, content={"message": "Courses type should be list."}
        )
    else:
        for course in courses:
            if course["course_id"] != course_id:
                all_courses.append(course)
        conf.set_key_value("courses", all_courses)
        return JSONResponse(status_code=200, content={"message": "success"})


@app.delete(
    "/courses/{course_id}/{type}",
    tags=["course"],
    summary="Delete a course item",
    description="Delete a course item. It will delete the course item with the given course id and type.",
)
async def delete_course_item(course_id: int, type: str):
    if "courses" not in conf.get_conf():
        return JSONResponse(status_code=404, content={"message": "Courses not found"})
    courses = conf.get_conf()["courses"]
    all_courses = []
    if not isinstance(courses, List):
        JSONResponse(
            status_code=404, content={"message": "Courses type should be list"}
        )
    else:
        for course in courses:
            if course["course_id"] != course_id or course["type"] != type:
                all_courses.append(course)
        conf.set_key_value("courses", all_courses)
        return JSONResponse(status_code=200, content={"message": "success"})


@app.post(
    "/courses", tags=["course"], summary="Add a course", description="Add a course."
)
async def create_course(course: Course):
    if course.type not in ["ann", "dis", "ass"]:
        return JSONResponse(status_code=400, content={"message": "Invalid course type"})
    if course.name == "":
        return JSONResponse(status_code=400, content={"message": "Empty course name"})
    course_info = {
        "course_id": course.id,
        "course_name": course.name,
        "type": course.type,
        "maxshow": course.maxshow,
        "order": course.order,
        "msg": course.msg,
    }
    if "courses" not in conf.get_conf():
        ori_courses = []
    else:
        ori_courses = conf.get_conf()["courses"]
    # Check if the course already exists
    if not isinstance(ori_courses, List):
        JSONResponse(
            status_code=404, content={"message": "Courses type should be list."}
        )
    else:
        for c in ori_courses:
            if c["course_id"] == course.id and c["type"] == course.type:
                return JSONResponse(
                    status_code=400, content={"message": "Course already exists"}
                )
        ori_courses.append(course_info)
        conf.set_key_value("courses", ori_courses)
        return JSONResponse(status_code=200, content={"message": "success"})


@app.put(
    "/courses",
    tags=["course"],
    summary="Modify a course",
    description="Modify a course.",
)
async def modify_course(index: int, course: Course):
    if "courses" not in conf.get_conf():
        return JSONResponse(status_code=404, content={"message": "Courses not found"})
    courses = conf.get_conf()["courses"]
    if not isinstance(courses, List):
        return JSONResponse(
            status_code=404, content={"message": "Courses type should be list"}
        )
    if index >= len(courses) or index < 0:
        return JSONResponse(status_code=404, content={"message": "Course not found"})
    if course.type not in ["ann", "ass", "dis"]:
        return JSONResponse(status_code=400, content={"message": "Invalid course type"})
    if course.name == "":
        return JSONResponse(status_code=400, content={"message": "Empty course name"})
    course_info = {
        "course_id": course.id,
        "course_name": course.name,
        "type": course.type,
        "maxshow": course.maxshow,
        "order": course.order,
        "msg": course.msg,
    }
    # Test if the course already exists
    for i in range(len(courses)):
        if (
            i != index
            and courses[i]["course_id"] == course.id
            and courses[i]["type"] == course.type
        ):
            return JSONResponse(
                status_code=400, content={"message": "Course already exists"}
            )

    courses[index] = course_info
    conf.set_key_value("courses", courses)
    return JSONResponse(status_code=200, content={"message": "success"})


@app.get(
    "/canvas/dashboard",
    tags=["canvas"],
    summary="Get the dashboard",
    description="Get the dashboard.",
)
async def get_dashboard(cache: bool = False, mode: str = "html"):
    if cache:
        # Use cache
        if path.exists("./canvas/cache.json"):
            with open(
                "./canvas/cache.json", "r", encoding="utf-8", errors="ignore"
            ) as f:
                obj = json.load(f)
                if mode == "html":
                    return {"data": obj["html"]}
                elif mode == "json":
                    return {"data": obj["json"]}
                else:
                    return JSONResponse(
                        status_code=400, content={"message": "Mode not supported"}
                    )
        else:
            return JSONResponse(status_code=404, content={"message": "Cache not found"})
    # No cache
    canvas = CanvasMGR(mode)
    return {"data": canvas.get_response()}


@app.post(
    "/canvas/check/{name}",
    tags=["canvas"],
    summary="Check some task",
    description="Check some task.",
)
async def set_check(name: str, check: Check):
    """
    Check

    Only 1,2,3 is available
    """
    if check.type < 0 or check.type > 3:
        return JSONResponse(status_code=400, content={"message": "Invalid check type"})
    all_checks = [{"name": name, "type": check.type}]
    if "checks" in conf.get_conf():
        ori_checks = conf.get_conf()["checks"]
        if not isinstance(ori_checks, List):
            return JSONResponse(
                status_code=404, content={"message": "Courses type should be list"}
            )
        for ori_check in ori_checks:
            if ori_check["name"] != name:
                all_checks.append(ori_check)
    conf.set_key_value("checks", all_checks)
    return JSONResponse(status_code=200, content={"message": "success"})


@app.get(
    "/canvas/position",
    tags=["canvas"],
    summary="Get the position",
    description="Get the position.",
)
async def get_position():
    """
    Get position
    """
    if "position" not in conf.configuration:
        return JSONResponse(status_code=404, content={"message": "Position not found"})
    return conf.get_conf()["position"]


@app.put(
    "/canvas/position",
    tags=["canvas"],
    summary="Set the position",
    description="Set the position.",
)
async def update_position(position: Position):
    """
    Set position
    """
    conf.set_key_value(
        "position",
        {
            "left": position.left,
            "top": position.top,
            "width": position.width,
            "height": position.height,
        },
    )
    return JSONResponse(status_code=200, content={"message": "success"})


@app.post(
    "/file/upload",
    tags=["file"],
    summary="Upload file",
    description="Upload file to public/res.",
)
async def upload_file(file: UploadFile):
    if not path.exists("./public/res"):
        mkdir("./public/res")
    tmp = check_file(file.filename)
    if tmp == "Illegal":
        return JSONResponse(status_code=404, content={"message": "Illegal file name"})
    with open(f"./public/res/{file.filename}", "wb") as out_file:
        out_file.write(file.file.read())
    return JSONResponse(status_code=200, content={"message": "success"})


@app.delete(
    "/file",
    tags=["file"],
    summary="Delete file",
    description="Delete file in public/res.",
)
async def delete_file(name: str):
    tmp = check_file(name)
    if tmp == "Illegal":
        return JSONResponse(status_code=404, content={"message": "Illegal file name"})
    if path.exists(f"./public/res/{name}"):
        remove(f"./public/res/{name}")
        return JSONResponse(status_code=200, content={"message": "success"})
    else:
        return JSONResponse(status_code=404, content={"message": "File not found"})


@app.get(
    "/file",
    tags=["file"],
    summary="Get file list",
    description="Get files in public/res.",
)
async def get_file_list():
    if path.exists("./public/res"):
        return {"files": listdir("./public/res")}
    else:
        mkdir("./public/res")
        return {"files": []}


@app.get(
    "/file/{name}",
    tags=["file"],
    summary="Get file",
    description="Get file in public/res.",
)
async def get_file(name: str):
    if path.exists(f"./public/res/{name}"):
        return FileResponse(f"./public/res/{name}")
    else:
        return JSONResponse(status_code=404, content={"message": "File not found"})


@app.post(
    "/browser",
    tags=["misc"],
    summary="Open URL in web browser",
    description="Open URL in web browser.",
)
async def open_url(data: URL):
    import webbrowser

    try:
        if data.browser:
            res = webbrowser.get(data.browser).open(data.url)
        else:
            res = webbrowser.open(data.url)
        if not res:
            raise Exception("Cannot find web browser")
        return JSONResponse(status_code=200, content={"message": "Opened"})
    except Exception as e:
        logging.warning(e)
        return JSONResponse(status_code=400, content={"message": "Failed to open"})


if __name__ == "__main__":
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
    uvicorn.run(f"{name_app}:app", port=9283, reload=False, log_config=log_config)
