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
from config_mgr import ConfigMGR
from canvas_mgr import CanvasMGR
from models import Position, Check, Course
from fastapi.responses import JSONResponse
from os import path
import json

app = FastAPI()
conf = ConfigMGR()


@app.get("/config")
async def get_configuration():
    return conf.get_conf()

@app.get("/config/refresh")
async def refresh_conf():
    conf.force_read()
    return JSONResponse(status_code=200, content={"message": "success"})

@app.get("/config/{key}")
async def get_configuration(key: str):
    if key not in conf.get_conf():
        return JSONResponse(status_code=404, content={"message": "Key not found"})
    return conf.get_conf()[key]

@app.put("/config/{key}")
async def update_configuration(key: str, request: Request):
    body = await request.body()
    try:
        body_p = json.loads('{"data" : ' + body.decode(encoding='utf-8') +'}')
    except:
        return JSONResponse(status_code=400, content={"message": "Cannot parse body"})
    conf.set_key_value(key, body_p["data"])
    return JSONResponse(status_code=200, content={"message": "success"})

@app.delete("/config/{key}")
async def delete_configuration(key: str):
    if key not in conf.get_conf():
        return JSONResponse(status_code=404, content={"message": "Key not found"})
    conf.remove_key(key)
    return JSONResponse(status_code=200, content={"message": "success"})

@app.get("/courses")
async def get_all_courses():
    if not "courses" in conf.get_conf():
        return JSONResponse(status_code=404, content={"message": "Courses not found"})
    return conf.get_conf()["courses"]

@app.delete("/courses/{course_id}")
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

@app.delete("/courses/{course_id}/{type}")
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

@app.post("/courses")
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
    ori_courses.append(course_info)
    conf.set_key_value("courses", ori_courses)
    return JSONResponse(status_code=200, content={"message": "success"})

@app.get("/canvas/dashboard")
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


@app.post("/canvas/check")
async def set_check(check: Check):
    '''
    Check

    Only 1,2,3 is available
    '''
    if check.type == None or check.type <= 0 or check.type >= 4:
        return JSONResponse(status_code=400, content={"message": "Invalid check type"})
    all_checks = [{"name": check.name, "type": check.type}]
    if "checks" in conf.get_conf():
        ori_checks = conf.get_conf()["checks"]
        for ori_check in ori_checks:
            if ori_check["name"] != check.name:
                all_checks.append(ori_check)
    conf.set_key_value("checks", all_checks)
    return JSONResponse(status_code=200, content={"message": "success"})


@app.delete("/canvas/check")
async def delete_check(check: Check):
    '''
    Delete check
    '''
    if not "checks" in conf.get_conf():
        # No check
        return JSONResponse(status_code=404, content={"message": "No check available"})
    ori_checks = conf.get_conf()["checks"]
    all_checks = []
    for ch in ori_checks:
        if ch["name"] != check.name:
            # Not Matched!
            all_checks.append(ch)
    conf.set_key_value("checks", all_checks)
    return JSONResponse(status_code=200, content={"message": "success"})


@app.get("/canvas/position")
async def get_position():
    '''
    Get position
    '''
    if "position" not in conf.configuration:
        return JSONResponse(status_code=404, content={"message": "Position not found"})
    return conf.get_conf()["position"]


@app.put("/canvas/position")
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
