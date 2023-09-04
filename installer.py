#!/usr/bin/env python3

import tkinter as tk
import os

"""
Auto Setup

This file can offer a gui for user
to set the host, port and auto-start
"""


def net_conf(host, port, system_name):
    base = os.path.dirname(__file__)
    net_config_path = f"{base}/net_config.txt"
    net_config_content = f"""
    host:{host},
    port:{port}
    """

    with open(net_config_path, "w") as net_config:
        net_config.write(net_config_content)

    if system_name == "windows":
        win()
    elif system_name == "linux":
        linux()
    else:
        mac()

    root.destroy()


def win():
    current_drive = os.path.abspath(__file__)[0]
    app_path = os.getenv("APPDATA")

    # WARNING: Fail to get the path
    if app_path is None:
        print(
            "Fail to get the APPDATA's path. See readme and solve the problem manually"
        )
        return

    startup_folder = os.path.join(
        app_path, "Microsoft\\Windows\\Start Menu\\Programs\\Startup"
    )
    vbs_script_path = os.path.join(startup_folder, "canvashelper.vbs")
    bat_script_dir = os.path.abspath(__file__)
    bat_script_path = os.path.join(os.path.abspath(__file__), "canvashelper.bat")

    # TEST: VBS
    vbs_script_content = f"""
    Dim WinScriptHost
    Set WinScriptHost = CreateObject("WScript.Shell")
    WinScriptHost.Run Chr(34) & "{bat_script_path}" & Chr(34), 0
    Set WinScriptHost = Nothing
    """

    # TEST: Bat
    bat_script_content = f"""
    @echo off
    {current_drive}
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
    startup_folder = os.path.dirname(__file__)
    service_name = "/etc/systemd/system/canvashelper"
    service_path = f"{service_name}.service"

    # TEST: systemd unit
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

    os.system(f"sudo systemctl enable {service_name}")
    os.system(f"sudo systemctl start {service_name}")

    print("Success")


def mac():
    # INFO: Get path of files
    user_home = os.path.expanduser("~")
    launch_path = f"{user_home}/Library/LaunchAgents/canvashelper.plist"
    startup_folder = os.path.dirname(__file__)

    # TEST: plist
    plist_content = f"""
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>Label</key>
        <string>com.example.myscript</string>
        <key>ProgramArguments</key>
        <array>
            <string>{startup_folder}/start</string>
        </array>
        <key>RunAtLoad</key>
        <true/>
    </dict>
    </plist>
    """

    with open(launch_path, "w") as plist_file:
        plist_file.write(plist_content)

    os.system(f"launchctl load {launch_path}")

    print("Success")


root = tk.Tk()
root.title("Auto Setup")

system_label = tk.Label(root, text="Choose the system")
system_label.pack()

system_var = tk.StringVar()
system_var.set("Windows")

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
    command=lambda: net_conf(system_var.get(), host_entry.get(), port_entry.get()),
)
save_button.pack()

root.mainloop()
