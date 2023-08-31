import tkinter as tk
import os

def win():

    vbs_script_path = ""
    bat_script_path = os.path.abspath(__file__)

# 生成 VBS 脚本内容
    vbs_script_content = """
    Dim WinScriptHost
    Set WinScriptHost = CreateObject("WScript.Shell")
    WinScriptHost.Run Chr(34) & "C:\\XXX\\canvashelper.bat" & Chr(34), 0
    Set WinScriptHost = Nothing
    """

# 生成 BAT 脚本内容
    bat_script_content = """
    @echo off
    d:
    cd D:\\Project\\CanvasHelper2
    uvicorn canvas_app:app --port 9283
    """

# 将生成的内容写入文件
    with open(vbs_script_path, "w") as vbs_file:
        vbs_file.write(vbs_script_content)

    with open(bat_script_path, "w") as bat_file:
        bat_file.write(bat_script_content)

    print("脚本已生成并保存到指定路径。")

def on_item_selected(event):
    selected_item = listbox.get(listbox.curselection())
    selection_label.config(text=f"Selected: {selected_item}")
    if selected_item=="windows":
        pass
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

