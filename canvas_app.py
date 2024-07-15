#!/usr/bin/env python3

from fastapi import FastAPI, Request, UploadFile, Security, HTTPException, Depends, status
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from os import path, listdir, remove, mkdir
import uvicorn
from uvicorn.config import LOGGING_CONFIG
from jose import jwt, JWTError  # pip install python-jose
from typing import List
import requests
import json

from global_config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, ALGORITHM, uvicorn_domain, uvicorn_port, NUM_OF_THREADS, RELOAD
from auth import SECRET_KEY, timedelta, verify_login, authenticate_user, create_access_token, create_refresh_token
from local_func import check_file, htmlspecialchars, init_conf_path, url_format
from models import Check, Course, RequestForm
from users import create_user, user_exists
from config_mgr import ConfigMGR
from canvas_mgr import CanvasMGR
from cache_mgr import get_cache
from updater import update
"""
Canvas App

This file contains all the APIs to access the
configuration file/canvas backend, etc..
"""

app = FastAPI(version="1.0.1",
              title="Canvas Helper",
              description="Canvas Helper API.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

conf = ConfigMGR()

# Make sure all folders exist
init_conf_path()

# Self Update
update()


def verify_token(auth_token: str = Security(oauth2_scheme)):
    # Same as verify_login, but for interface dependency
    username = verify_login(auth_token)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authenticated",
                            headers={"WWW-Authenticate": "Bearer"})
    return username


def verify_bid(url, bid):
    headers = {"Authorization": f'Bearer {bid}'}
    url = url_format(url) + "api/v1/accounts"
    res = requests.get(url, headers=headers).status_code
    return res == 200


# Endpoints
@app.post(
    "/signup",
    summary="Sign up",
    description="Sign up",
    tags=["auth"],
)
async def signup(form_data: RequestForm):
    print("Signup: " + form_data.username)
    if user_exists(form_data.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    if not verify_bid(form_data.url, form_data.bid):
        raise HTTPException(status_code=400, detail="Invalid bid")
    create_user(form_data.username, form_data.password)
    return {"message": "Signed up"}


@app.post(
    "/login",
    summary="Login",
    description="Login",
    tags=["auth"],
)
async def login(form_data: RequestForm,
                auth_token: str = Security(oauth2_scheme)):
    if verify_login(auth_token):
        # Return HTML to avoid POST to GET conversion
        html_content = '<script>location.href = "."</script>'
        return HTMLResponse(content=html_content,
                            status_code=status.HTTP_200_OK)

    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400,
                            detail="Incorrect username or password")

    # Generate access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={
        "sub": user,
        "type": "access_token"
    },
                                       expires_delta=access_token_expires)

    # Generate refresh token
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(data={
        "sub": user,
        "type": "refresh_token"
    },
                                         expires_delta=refresh_token_expires)

    return JSONResponse(content={
        "message": "Logged in",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    },
                        status_code=status.HTTP_200_OK)


@app.post(
    "/refresh",
    summary="Refresh the access token",
    description="Refresh the access token",
    tags=["auth"],
    dependencies=[Depends(verify_token)],
)
async def refresh_token(form_data: RequestForm):
    refresh_token = form_data.password  # Actually refresh_token, but treated as secure as password
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh_token":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Invalid refresh token")
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Not authenticated")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid refresh token")

    # Generate new access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(data={
        "sub": username,
        "type": "access_token"
    },
                                           expires_delta=access_token_expires)

    return JSONResponse(content={
        "message": "Refreshed token",
        "new_access_token": new_access_token,
    },
                        status_code=status.HTTP_200_OK)


@app.get("/users/me")
async def read_users_me(current_user: dict = Depends(verify_token)):
    return current_user


@app.get(
    "/config",
    summary="Get the configuration file",
    description="Get the configuration file.",
    tags=["config"],
    dependencies=[Depends(verify_token)],
)
async def get_configuration(username: str = Depends(verify_token)):
    return conf.get_conf(username)


@app.get(
    "/config/refresh",
    tags=["config"],
    summary="Refresh the configuration file",
    description="Force to read the configuration file from disk.",
    dependencies=[Depends(verify_token)],
)
async def refresh_conf(username: str = Depends(verify_token)):
    conf.force_read(username)
    return JSONResponse(status_code=200, content={"message": "success"})


@app.get(
    "/config/key/{key}",
    tags=["config"],
    summary="Get a specific key from the configuration file",
    description="Get a specific key from the configuration file.",
    dependencies=[Depends(verify_token)],
)
async def get_configuration_key(key: str,
                                username: str = Depends(verify_token)):
    conf_content = conf.get_conf(username)
    if key not in conf_content:
        return JSONResponse(status_code=404,
                            content={"message": "Key not found"})
    return conf_content[key]


@app.put(
    "/config/key/{key}",
    tags=["config"],
    summary="Update a specific key in the configuration file",
    description="Update a specific key in the configuration file.",
    dependencies=[Depends(verify_token)],
)
async def update_configuration(key: str,
                               request: Request,
                               username: str = Depends(verify_token)):
    body = await request.body()
    try:
        body_p = json.loads('{"data" : ' + body.decode(encoding="utf-8") + "}")
    except:
        return JSONResponse(status_code=400,
                            content={"message": "Cannot parse body"})
    conf.set_key_value(username, key, body_p["data"])
    return JSONResponse(status_code=200, content={"message": "success"})


@app.delete(
    "/config/key/{key}",
    tags=["config"],
    summary="Delete a specific key in the configuration file",
    description="Delete a specific key in the configuration file.",
    dependencies=[Depends(verify_token)],
)
async def delete_configuration(key: str,
                               username: str = Depends(verify_token)):
    if key not in conf.get_conf(username):
        return JSONResponse(status_code=404,
                            content={"message": "Key not found"})
    conf.remove_key(username, key)
    return JSONResponse(status_code=200, content={"message": "success"})


@app.get(
    "/config/verify",
    tags=["config"],
    summary="Verify the configuration file",
    description="Verify the configuration file.",
    dependencies=[Depends(verify_token)],
)
async def verify_config(username: str = Depends(verify_token)):
    conf_content = conf.get_conf(username)
    """
    Verify the configuration
    """
    if "bid" not in conf_content:
        return JSONResponse(status_code=404,
                            content={"message": "bid not found"})
    if "url" not in conf_content:
        return JSONResponse(status_code=404,
                            content={"message": "url not found"})
    if "background_image" not in conf_content and "video" not in conf_content:
        return JSONResponse(status_code=400,
                            content={"message": "background not set"})
    # Test bid
    url = conf_content["url"]
    # conf.set_key_value(username, "url", url)
    if verify_bid(url, conf_content["bid"]):
        return JSONResponse(status_code=200, content={"message": "success"})
    else:
        return JSONResponse(status_code=400,
                            content={"message": "verification failed"})


@app.get(
    "/courses",
    tags=["course"],
    summary="Get all the courses",
    description="Get all the courses.",
    dependencies=[Depends(verify_token)],
)
async def get_all_courses(username: str = Depends(verify_token)):
    conf_content = conf.get_conf(username)

    if "courses" not in conf_content:
        return []
    return conf_content["courses"]


@app.get(
    "/courses/canvas",
    tags=["course"],
    summary="Get all the courses from canvas",
    description="Get all the courses from canvas.",
    dependencies=[Depends(verify_token)],
)
async def get_all_canvas_courses(username: str = Depends(verify_token)):
    conf_content = conf.get_conf(username)

    if "bid" not in conf_content:
        return JSONResponse(status_code=404,
                            content={"message": "bid not found"})

    headers = {"Authorization": f'Bearer {conf_content["bid"]}'}
    url = url_format(conf_content["url"]) + "api/v1/dashboard/dashboard_cards"
    res = requests.get(url, headers=headers).text
    return json.loads(res)


@app.delete(
    "/courses/{course_id}",
    tags=["course"],
    summary="Delete a course",
    description=
    "Delete a course. It will delete all the course items with the given course id.",
    dependencies=[Depends(verify_token)],
)
async def delete_course(course_id: int, username: str = Depends(verify_token)):
    conf_content = conf.get_conf(username)

    if "courses" not in conf_content:
        return JSONResponse(status_code=404,
                            content={"message": "Courses not found"})
    courses = conf_content["courses"]
    all_courses = []
    if not isinstance(courses, List):
        return JSONResponse(
            status_code=404,
            content={"message": "Courses type should be list."})
    else:
        for course in courses:
            if course["course_id"] != course_id:
                all_courses.append(course)
        conf.set_key_value(username, "courses", all_courses)
        return JSONResponse(status_code=200, content={"message": "success"})


@app.delete(
    "/courses/{course_id}/{type}",
    tags=["course"],
    summary="Delete a course item",
    description=
    "Delete a course item. It will delete the course item with the given course id and type.",
    dependencies=[Depends(verify_token)],
)
async def delete_course_item(course_id: int,
                             type: str,
                             username: str = Depends(verify_token)):
    conf_content = conf.get_conf(username)

    if "courses" not in conf_content:
        return JSONResponse(status_code=404,
                            content={"message": "Courses not found"})
    courses = conf_content["courses"]
    all_courses = []
    if not isinstance(courses, List):
        JSONResponse(status_code=404,
                     content={"message": "Courses type should be list"})
    else:
        for course in courses:
            if course["course_id"] != course_id or course["type"] != type:
                all_courses.append(course)
        conf.set_key_value(username, "courses", all_courses)
        return JSONResponse(status_code=200, content={"message": "success"})


@app.post(
    "/courses",
    tags=["course"],
    summary="Add a course",
    description="Add a course.",
    dependencies=[Depends(verify_token)],
)
async def create_course(course: Course, username: str = Depends(verify_token)):
    conf_content = conf.get_conf(username)

    if course.type not in [0, 1, 2]:
        return JSONResponse(status_code=400,
                            content={"message": "Invalid course type"})
    if course.name == "":
        return JSONResponse(status_code=400,
                            content={"message": "Empty course name"})
    course_info = {
        "course_id": course.id,
        "course_name": htmlspecialchars(course.name),  # XSS protection
        "type": course.type,
        "maxshow": course.maxshow,
        "order": course.order,
        "msg": htmlspecialchars(course.msg),
    }
    if "courses" not in conf_content:
        ori_courses = []
    else:
        ori_courses = conf_content["courses"]
    # Check if the course already exists
    if not isinstance(ori_courses, List):
        JSONResponse(status_code=404,
                     content={"message": "Courses type should be list."})
    else:
        for c in ori_courses:
            if c["course_id"] == course.id and c["type"] == course.type:
                return JSONResponse(
                    status_code=400,
                    content={"message": "Course already exists"})
        ori_courses.append(course_info)
        conf.set_key_value(username, "courses", ori_courses)
        return JSONResponse(status_code=200, content={"message": "success"})


@app.put(
    "/courses",
    tags=["course"],
    summary="Modify a course",
    description="Modify a course.",
    dependencies=[Depends(verify_token)],
)
async def modify_course(index: int,
                        course: Course,
                        username: str = Depends(verify_token)):
    conf_content = conf.get_conf(username)

    if "courses" not in conf_content:
        return JSONResponse(status_code=404,
                            content={"message": "Courses not found"})
    courses = conf_content["courses"]
    if not isinstance(courses, List):
        return JSONResponse(status_code=404,
                            content={"message": "Courses type should be list"})
    if index >= len(courses) or index < 0:
        return JSONResponse(status_code=404,
                            content={"message": "Course not found"})
    if course.type not in [0, 1, 2]:
        return JSONResponse(status_code=400,
                            content={"message": "Invalid course type"})
    if course.name == "":
        return JSONResponse(status_code=400,
                            content={"message": "Empty course name"})
    course_info = {
        "course_id": course.id,
        "course_name": htmlspecialchars(course.name),  # XSS protection
        "type": course.type,
        "maxshow": course.maxshow,
        "order": course.order,
        "msg": htmlspecialchars(course.msg),
    }
    # Test if the course already exists
    for i in range(len(courses)):
        if (i != index and courses[i]["course_id"] == course.id
                and courses[i]["type"] == course.type):
            return JSONResponse(status_code=400,
                                content={"message": "Course already exists"})

    courses[index] = course_info
    conf.set_key_value(username, "courses", courses)
    return JSONResponse(status_code=200, content={"message": "success"})


@app.get(
    "/canvas/dashboard",
    tags=["canvas"],
    summary="Get the dashboard",
    description="Get the dashboard.",
    dependencies=[Depends(verify_token)],
)
async def get_dashboard(cache: bool = False,
                        username: str = Depends(verify_token)):
    if cache:
        cached_html = get_cache(username)
        if cached_html is not None:
            return {"data": cached_html}

    canvas = CanvasMGR(username)
    return {"data": canvas.get_response()}


@app.post(
    "/canvas/check/{item_id}",
    tags=["canvas"],
    summary="Check some task",
    description="Check some task.",
    dependencies=[Depends(verify_token)],
)
async def set_check(item_id,
                    check: Check,
                    username: str = Depends(verify_token)):
    # conf_content = conf.get_conf(username)
    """
    Check

    Only 1,2,3 is available
    """
    if check.type < 0 or check.type > 3:
        return JSONResponse(status_code=400,
                            content={"message": "Invalid check type"})
    all_checks = [{"item_id": item_id, "type": check.type}]
    # if "checks" in conf_content:
    #     ori_checks = conf_content["checks"]
    #     if not isinstance(ori_checks, List):
    #         return JSONResponse(
    #             status_code=404,
    #             content={"message": "Courses type should be list"})
    #     for ori_check in ori_checks:
    #         if ori_check["item_id"] != item_id:
    #             all_checks.append(ori_check)
    # TODO: check if the item exists to prevent XSS
    conf.set_key_value(username, "checks", all_checks)
    return JSONResponse(status_code=200, content={"message": "success"})


@app.post(
    "/file/upload",
    tags=["file"],
    summary="Upload file",
    description="Upload file to public/res.",
    dependencies=[Depends(verify_token)],
)
async def upload_file(file: UploadFile):
    if not path.exists("./public/res"):
        mkdir("./public/res")
    tmp = check_file(file.filename)
    if tmp == "Illegal":
        return JSONResponse(status_code=404,
                            content={"message": "Illegal file name"})
    with open(f"./public/res/{file.filename}", "wb") as out_file:
        out_file.write(file.file.read())
    return JSONResponse(status_code=200, content={"message": "success"})


@app.delete(
    "/file",
    tags=["file"],
    summary="Delete file",
    description="Delete file in public/res.",
    dependencies=[Depends(verify_token)],
)
async def delete_file(name: str):
    tmp = check_file(name)
    if tmp == "Illegal":
        return JSONResponse(status_code=404,
                            content={"message": "Illegal file name"})
    if path.exists(f"./public/res/{name}"):
        remove(f"./public/res/{name}")
        return JSONResponse(status_code=200, content={"message": "success"})
    else:
        return JSONResponse(status_code=404,
                            content={"message": "File not found"})


@app.get(
    "/file",
    tags=["file"],
    summary="Get file list",
    description="Get files in public/res.",
    dependencies=[Depends(verify_token)],
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
    # dependencies=[Depends(verify_token)],
)
async def get_file(name: str):
    if path.exists(f"./public/res/{name}"):
        return FileResponse(f"./public/res/{name}")
    else:
        return JSONResponse(status_code=404,
                            content={"message": "File not found"})


if __name__ == "__main__":
    LOGGING_CONFIG["formatters"]["default"][
        "fmt"] = "%(asctime)s %(levelprefix)s %(message)s"
    LOGGING_CONFIG["formatters"]["access"][
        "fmt"] = '%(asctime)s %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'
    uvicorn.run(
        app="canvas_app:app",
        host=uvicorn_domain,
        port=uvicorn_port,
        ssl_keyfile="key.pem" if path.exists("key.pem") else None,
        ssl_certfile="cert.pem" if path.exists("cert.pem") else None,
        log_config=LOGGING_CONFIG,
        workers=NUM_OF_THREADS,
        reload=RELOAD,
    )
