#!/usr/bin/env python3

import json
from getpass import getuser
from subprocess import Popen,PIPE
import os

def win():
    user_name = getuser()

    if user_name is None:
        print("Fail to get the User Name. See readme and solve the problem manually")
        exit(1)

    startup_folder = f"C:\\Users\\{user_name}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"

    vbs_script_path = f"{startup_folder}\\canvashelper.vbs"
    # INFO: Removing files

    os.system(f"del {vbs_script_path}")
    os.system("del ./canvashelper.bat")

#PASSED: Tested on macos Ventura 13.3.1
def mac():
    user_home = os.path.expanduser("~")
    launch_path = f"{user_home}/Library/LaunchAgents/com.canvashelper.service.plist"

    ret,_=Popen("launchctl list|grep canvas", shell=True, stdout=PIPE).communicate()
    if ret.decode("utf-8").strip() is not None:
        os.system(f"launchctl unload {launch_path}")
    os.system(f"rm {launch_path}")

#PASSED: Tested on docker unbuntu 20.04
def linux():
    service_name = "/etc/systemd/system/canvashelper"
    service_path = f"{service_name}.service"

    os.system("systemctl stop canvashelper.service")
    os.system("systemctl disable canvashelper.service")
    os.system(f"rm {service_path}")

config={}

with open("./net_config.json", "r", encoding="utf-8", errors="ignore") as f:
    config=json.load(f)

if config["system"] == "win":
    win()

elif config["system"] == "mac":
    mac()

elif config["system"]=="linux":
    linux()

print("Success!")
