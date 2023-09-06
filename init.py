#!/usr/bin/env python3

import tkinter as tk
from getpass import getuser
import os
import json
from subprocess import Popen, PIPE

"""
Auto Setup

This file can offer a gui for user to set
(or reset) the host, port and auto-start
"""


def net_conf(host, port, system_name):
    net_config = {
        "system": system_name,
        "host": host,
        "port": port,
    }
    with open("./net_config.json", "w", encoding="utf-8", errors="ignore") as f:
        json.dump(net_config, f, ensure_ascii=False, indent=4)

    if system_name == "win":
        win()
    elif system_name == "linux":
        linux()
    else:
        mac()

    root.destroy()


def win():
    current_drive = os.path.abspath(__file__)[0]
    user_name = getuser()

    if user_name is None:
        print("Fail to get the User Name. See readme and solve the problem manually")
        return

    startup_folder = f"C:\\Users\\{user_name}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"

    vbs_script_path = f"{startup_folder}\\canvashelper.vbs"
    bat_script_dir = os.getcwd()
    bat_script_path = os.path.join(bat_script_dir, "canvashelper.bat")

    # PASSED: VBS
    vbs_script_content = f"""
    Dim WinScriptHost
    Set WinScriptHost = CreateObject("WScript.Shell")
    WinScriptHost.Run Chr(34) & "{bat_script_path}" & Chr(34), 0
    Set WinScriptHost = Nothing
    """

    # PASSED: Bat
    bat_script_content = f"""
    @echo off
    {current_drive}:
    cd {bat_script_dir}
    ./start.py
    """

    # INFO: Write the file
    with open(vbs_script_path, "w") as vbs_file:
        vbs_file.write(vbs_script_content)

    with open(bat_script_path, "w") as bat_file:
        bat_file.write(bat_script_content)

    print("Success!")


def linux():
    # INFO: Get path of files
    startup_folder = os.getcwd()
    service_name = "/etc/systemd/system/canvashelper"
    service_path = f"{service_name}.service"

    # PASSED: systemd unit
    systemd_content = f"""
    [Unit]
    Description=Auto Setup for canvashelper

    [Service]
    ExecStart={startup_folder}/start
    WorkingDirectory={startup_folder}
    Restart=always

    [Install]
    WantedBy=multi-user.target
    """

    with open(service_path, "w") as service_file:
        service_file.write(systemd_content)

    os.system(f"sudo systemctl enable canvashelper.service")
    os.system(f"sudo systemctl start canvashelper.service")

    print("Success")


def mac():
    # INFO: Get path of files
    user_home = os.path.expanduser("~")
    launch_path = f"{user_home}/Library/LaunchAgents/com.canvashelper.service.plist"
    startup_folder = os.getcwd()

    # PASSED: plist
    plist_content = f"""
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>

        <key>Label</key>
        <string>com.canvashelper.service</string>

        <key>WorkingDirectory</key>
        <string>{startup_folder}</string>

        <key>ProgramArguments</key>
        <array>
            <string>{startup_folder}/start</string>
        </array>

        <key>RunAtLoad</key>
        <true/>

        <key>KeepAlive</key>
        <true/>

    </dict>
    </plist>
    """

    with open(launch_path, "w") as plist_file:
        plist_file.write(plist_content)

    ret, _ = Popen("launchctl list|grep canvas", shell=True, stdout=PIPE).communicate()
    if ret.decode("utf-8").strip() is not None:
        os.system(f"launchctl unload {launch_path}")

    os.system(f"launchctl load -w {launch_path}")
    os.system(f"launchctl start {launch_path}")

    print("Success")


root = tk.Tk()
root.title("Auto Setup")

system_label = tk.Label(root, text="Choose the system")
system_label.pack()

system_var = tk.StringVar()
system_var.set("Select your system")

system_option_menu = tk.OptionMenu(root, system_var, "win", "linux", "mac")
system_option_menu.pack()

host_label = tk.Label(root, text="host")
host_label.pack()

host_entry = tk.Entry(root)
host_entry.pack()

port_label = tk.Label(root, text="port")
port_label.pack()

port_entry = tk.Entry(root)
port_entry.pack()

save_button = tk.Button(
    root,
    text="save",
    command=lambda: net_conf(host_entry.get(), port_entry.get(), system_var.get()),
)
save_button.pack()

root.mainloop()
