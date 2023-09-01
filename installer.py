import tkinter as tk
import os
import platform

def win():
    current_drive=os.path.abspath(__file__)[0]
    app_path=os.getenv('APPDATA')

    #WARNING: Fail to get the path
    if app_path is None:
        print("Fail to get the APPDATA's path. See readme and solve the problem manually")
        return

    startup_folder = os.path.join(app_path, 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
    vbs_script_path = os.path.join(startup_folder, 'canvashelper.vbs')
    bat_script_dir = os.path.abspath(__file__)
    bat_script_path = os.path.join(os.path.abspath(__file__), "canvashelper.bat")

    #TEST: VBS
    vbs_script_content = f"""
    Dim WinScriptHost
    Set WinScriptHost = CreateObject("WScript.Shell")
    WinScriptHost.Run Chr(34) & "{bat_script_path}" & Chr(34), 0
    Set WinScriptHost = Nothing
    """

    #TEST: Bat
    bat_script_content = f"""
    @echo off
    {current_drive}
    cd {bat_script_dir}
    uvicorn canvas_app:app --port 9283
    """

    #INFO: Write the file
    with open(vbs_script_path, "w") as vbs_file:
        vbs_file.write(vbs_script_content)

    with open(bat_script_path, "w") as bat_file:
        bat_file.write(bat_script_content)

    print("Success!")

def linux():
    pass

def mac():
    pass


def on_item_selected(events):
    selected_item = listbox.get(listbox.curselection())
    selection_label.config(text=f"Selected: {selected_item}")
    if selected_item=="windows":
       win() 
    elif selected_item=="linux":
        pass
    else:
        pass

root = tk.Tk()
root.title("Listbox Example")

listbox = tk.Listbox(root)
listbox.pack(padx=20, pady=20)

items = ["linux", "windows", "macos"]
for item in items:
    listbox.insert(tk.END, item)

selection_label = tk.Label(root, text="Selected: ")
selection_label.pack()

listbox.bind("<<ListboxSelect>>", on_item_selected)

# 运行主循环
root.mainloop()

