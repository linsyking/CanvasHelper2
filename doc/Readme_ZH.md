# Canvas Helper 2

[![build](https://github.com/linsyking/CanvasHelper2/actions/workflows/build.yml/badge.svg)](https://github.com/linsyking/CanvasHelper2/actions/workflows/build.yml)

新一代canvas helper后端。
基于网页，支持Windows, Macos, linux。

## 目录

- [要求](#要求)
- [部署](#部署)
- [常见问题](#常见问题)
- [开发](#开发)

## 要求

- Python >= 3.7

## 部署

1. [运行后端](#运行后端)
2. [打开前端，进行配置](#配置canvashelper)
3. [网页上查看效果](#预览效果)

### 运行后端

首先，克隆本仓库并进入仓库：

    ```bash
    git clone https://github.com/linsyking/CanvasHelper2.git

    cd CanvasHelper2
    ```

下载依赖项：

    ```bash
    pip3 install -r requirements.txt
    ```

如果你不想改变任何设置，（例如 CORS），你可以直接运行（如果你想使用我们服务器上的前端，你必须使用`9283`端口）：

    ```bash
    uvicorn canvas_app:app --port 9283
    ```

### 配置CanvasHelper

如果你想使用我们的服务器，可以访问[here](https://canvashelper2.web.app/canvashelper/)。（网站位置未来可能会变动）

如果你想使用自己的前端，你可以参照[CanvasHelper2-conf](https://github.com/linsyking/CanvasHelper2-conf)来获取更多信息

### 预览效果

如果你想在不托管HTML文件的前提下预览效果，你可以直接访问[here](https://canvashelper2.web.app/)。

如果你想在本地查看dashboard，你可以使用任意端口托管静态文件

一个dashboard样例在<https://github.com/linsyking/CanvasHelper2-dashboard>.

你可以克隆此仓库并使用：

    ```bash
    python3 -m http.server 9282
    ```

来托管静态html文件，并在<http://localhost:9282>查看结果

### 部署到桌面

#### Wallpaper Engine

订阅壁纸：<https://steamcommunity.com/sharedfiles/filedetails/?id=2913474561>

在本地运行后端后，它将会重定向到[here](https://canvashelper2.web.app/)。你也可以把它改成你本地的前端

如果你想在开始时就运行后端，你可以参考以下步骤：

1. Win+R, 输入`shell:startup`
2. 在打开的窗口中创建一个叫做`canvashelper.vbs`的文件，它的内容如下：

    ```vbs
    Dim WinScriptHost
    Set WinScriptHost = CreateObject("WScript.Shell")
    WinScriptHost.Run Chr(34) & "C:\XXX\canvashelper.bat" & Chr(34), 0
    Set WinScriptHost = Nothing
    ```

    将 `C:\XXX\canvashelper.bat` 替换成你用来存储启动CanvasHelper脚本的路径

    **这个脚本必须在C盘中**

3. 用以下内容创建`C:\XXX\canvashelper.bat`脚本：

    ```cmd
    @echo off

    d:
    cd D:\Project\CanvasHelper2
    uvicorn canvas_app:app --port 9283
    ```

    将`d:`和`D:\Project\CanvasHelper2`替换成你自己的目录

    （如果你在C盘中克隆本仓库，你不需要使用`d:`进入D盘）

    此后，你的系统将会在开机时自动运行此脚本

    **注意：有些特性在wallpaper engine中不能很好的支持，包括滚动**

#### KDE Wallpaper

1. 下载[wallpaper-engine-kde-plugin](https://github.com/catsout/wallpaper-engine-kde-plugin).
2. 下载canvas壁纸 <https://steamcommunity.com/sharedfiles/filedetails/?id=2913474561>。
3. 你应该能够看到壁纸
4. 添加开机脚本来运行后端

**注意：同样不支持滚动**

效果：

![demo](https://user-images.githubusercontent.com/49303317/210978732-68cefd73-75df-4013-a7cb-2010f16ec7dd.png)

#### KDE Widget

（另一个前端）

*To-Do*

## 常见问题

- CanvasHelper2和CanvasHelper1有什么区别

>CanvasHelper1是中心化的，而CanvasHelper2不是。它完全是本地的，所以你不需要连接到我们的服务器来使用CanvasHelper。
>此外，CanvasHelper2提供了一个方便的web界面来配置课程。
>CanvasHelper2将前端和后端分开，这样你就可以在任何操作系统/桌面环境下开发自己的dashboard前端。

- CanvasHelper后端，前端，dashboard的关系?

> 后端提供了一些API供前端和dashboard调用；前端使用本地的API来配置Canvas Helper。dashboard同样调用本地的后端获取配置文件。

- 我必须使用样板dashboard吗？

> 不，你可以开发你自己的dashboard。样板dashboard使用后端的html输出并在一个可以拖动的组件中展示。

## 开发

如果你想创建自己的前端或者支持本项目，你需要做一下三个步骤：

1. 运行后端
2. 运行`CanvasHelper2-conf`并在浏览器中配置Canvas Helper
3. 运行一个HTTP服务器以托管静态HTML文件（或者开发你自己的dashboard）

对于开发者，你可能需要使用以下代码在修改脚本后来重新加载api：

    ```bash
    uvicorn canvas_app:app --reload
    ```

如果你想要公开端口，你可以增加选项`--host 0.0.0.0`。
