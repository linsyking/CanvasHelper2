#!/usr/bin/env python3
'''
@Author: King
@Date: 2023-01-04 20:22:05
@Email: linsy_king@sjtu.edu.cn
@Url: https://yydbxx.cn
'''

'''
Canvas App

This file contains all the APIs to access the configuration file/canvas backend, etc..
'''

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from config_mgr import ConfigMGR
from canvas_mgr import CanvasMGR
from models import Position, Check, Course
from fastapi.responses import JSONResponse
from os import path
import json

app = FastAPI(version='0.1.0', title='Canvas Helper', description='Canvas Helper API.')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conf = ConfigMGR()


@app.get("/config", summary="Get the configuration file", description="Get the configuration file.", tags=["config"])
async def get_configuration():
    return conf.get_conf()

@app.get("/config/refresh",tags=["config"], summary="Refresh the configuration file", description="Force to read the configuration file from disk.")
async def refresh_conf():
    conf.force_read()
    return JSONResponse(status_code=200, content={"message": "success"})

@app.get("/config/key/{key}", tags=["config"], summary="Get a specific key from the configuration file", description="Get a specific key from the configuration file.")
async def get_configuration(key: str):
    if key not in conf.get_conf():
        return JSONResponse(status_code=404, content={"message": "Key not found"})
    return conf.get_conf()[key]

@app.put("/config/key/{key}", tags=["config"], summary="Update a specific key in the configuration file", description="Update a specific key in the configuration file.")
async def update_configuration(key: str, request: Request):
    body = await request.body()
    try:
        body_p = json.loads('{"data" : ' + body.decode(encoding='utf-8') +'}')
    except:
        return JSONResponse(status_code=400, content={"message": "Cannot parse body"})
    conf.set_key_value(key, body_p["data"])
    return JSONResponse(status_code=200, content={"message": "success"})

@app.delete("/config/key/{key}", tags=["config"], summary="Delete a specific key in the configuration file", description="Delete a specific key in the configuration file.")
async def delete_configuration(key: str):
    if key not in conf.get_conf():
        return JSONResponse(status_code=404, content={"message": "Key not found"})
    conf.remove_key(key)
    return JSONResponse(status_code=200, content={"message": "success"})

@app.get("/config/verify", tags=["config"])
async def verify_config():
    '''
    Verify the configuration
    '''
    if "bid" not in conf.get_conf():
        return JSONResponse(status_code=404, content={"message": "bid not found"})
    if "url" not in conf.get_conf():
        return JSONResponse(status_code=404, content={"message": "url not found"})
    # Test bid

    import requests

    headers = {
        'Authorization': f'Bearer {conf.get_conf()["bid"]}'
    }
    print(conf.get_conf()["url"])
    res = requests.get(path.join(conf.get_conf()["url"], 'api/v1/accounts'), headers=headers).status_code
    if res == 200:
        return JSONResponse(status_code=200, content={"message": "success"})
    else:
        return JSONResponse(status_code=400, content={"message": "Invalid bid"})

@app.get("/courses", tags=["course"], summary="Get all the courses", description="Get all the courses.")
async def get_all_courses():
    if not "courses" in conf.get_conf():
        return JSONResponse(status_code=404, content={"message": "Courses not found"})
    return conf.get_conf()["courses"]

@app.delete("/courses/{course_id}", tags=["course"], summary="Delete a course", description="Delete a course. It will delete all the course items with the given course id.")
async def delete_course(course_id: int):
    if not "courses" in conf.get_conf():
        return JSONResponse(status_code=404, content={"message": "Courses not found"})
    courses = conf.get_conf()["courses"]
    all_courses = []
    for course in courses:
        if course["course_id"] != course_id:
            all_courses.append(course)
    conf.set_key_value("courses", all_courses)
    return JSONResponse(status_code=200, content={"message": "success"})

@app.delete("/courses/{course_id}/{type}", tags=["course"], summary="Delete a course item", description="Delete a course item. It will delete the course item with the given course id and type.")
async def delete_course(course_id: int, type: str):
    if not "courses" in conf.get_conf():
        return JSONResponse(status_code=404, content={"message": "Courses not found"})
    courses = conf.get_conf()["courses"]
    all_courses = []
    for course in courses:
        if course["course_id"] != course_id or course["type"] != type:
            all_courses.append(course)
    conf.set_key_value("courses", all_courses)
    return JSONResponse(status_code=200, content={"message": "success"})

@app.post("/courses", tags=["course"], summary="Add a course", description="Add a course.")
async def create_course(course: Course):
    if course.type not in ['ann', 'dis', 'ass']:
        return JSONResponse(status_code=400, content={"message": "Invalid course type"})
    course_info = {
            "course_id": course.id,
            "course_name": course.name,
            "type": course.type
    }
    if course.maxshow:
        course_info["maxshow"] = course.maxshow
    if course.order:
        course_info["order"] = course.order
    if course.msg:
        course_info["msg"] = course.msg
    if not "courses" in conf.get_conf():
        ori_courses = []
    else:
        ori_courses = conf.get_conf()["courses"]
    # Check if the course already exists
    for c in ori_courses:
        if c["course_id"] == course.id and c["type"] == course.type:
            return JSONResponse(status_code=400, content={"message": "Course already exists"})
    ori_courses.append(course_info)
    conf.set_key_value("courses", ori_courses)
    return JSONResponse(status_code=200, content={"message": "success"})

@app.get("/canvas/dashboard", tags=["canvas"], summary="Get the dashboard", description="Get the dashboard.")
async def get_dashboard(cache: bool = False):
    if cache:
        # Use cache
        if path.exists('./canvas/cache.json'):
            with open('./canvas/cache.json', 'r') as f:
                return {"data": f.read()}
        else:
            return JSONResponse(status_code=404, content={"message": "Cache not found"})
    # No cache
    canvas = CanvasMGR()
    return {"data": canvas.get_response()}


@app.post("/canvas/check/{name}", tags=["canvas"], summary="Check some task", description="Check some task.")
async def set_check(name:str, check: Check):
    '''
    Check

    Only 1,2,3 is available
    '''
    if check.type == None or check.type <= 0 or check.type >= 4:
        return JSONResponse(status_code=400, content={"message": "Invalid check type"})
    all_checks = [{"name": name, "type": check.type}]
    if "checks" in conf.get_conf():
        ori_checks = conf.get_conf()["checks"]
        for ori_check in ori_checks:
            if ori_check["name"] != name:
                all_checks.append(ori_check)
    conf.set_key_value("checks", all_checks)
    return JSONResponse(status_code=200, content={"message": "success"})


@app.delete("/canvas/check/{name}", tags=["canvas"], summary="Delete a check", description="Delete a check.")
async def delete_check(name: str):
    '''
    Delete check
    '''
    if not "checks" in conf.get_conf():
        # No check
        return JSONResponse(status_code=404, content={"message": "No check available"})
    ori_checks = conf.get_conf()["checks"]
    all_checks = []
    for ch in ori_checks:
        if ch["name"] != name:
            # Not Matched!
            all_checks.append(ch)
    conf.set_key_value("checks", all_checks)
    return JSONResponse(status_code=200, content={"message": "success"})


@app.get("/canvas/position", tags=["canvas"], summary="Get the position", description="Get the position.")
async def get_position():
    '''
    Get position
    '''
    if "position" not in conf.configuration:
        return JSONResponse(status_code=404, content={"message": "Position not found"})
    return conf.get_conf()["position"]


@app.put("/canvas/position", tags=["canvas"], summary="Set the position", description="Set the position.")
async def update_position(position: Position):
    '''
    Set position
    '''
    conf.set_key_value("position", {
                       "left": position.left,
                       "top": position.top,
                       "width": position.width,
                       "height": position.height})
    return JSONResponse(status_code=200, content={"message": "success"})
