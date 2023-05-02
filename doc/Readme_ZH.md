# Canvas Helper 2

[![build](https://github.com/linsyking/CanvasHelper2/actions/workflows/build.yml/badge.svg)](https://github.com/linsyking/CanvasHelper2/actions/workflows/build.yml)

新一代的Canvas Helper后端。基于网页，支持Linux, Windows和MacOS。

## 要求

- Python >= 3.7

## 工作流程

如果你只想在本地运行后端，在我们的服务器上使用前端，请执行以下操作:

1. 根据[文档](https://github.com/linsyking/CanvasHelper2/blob/main/doc/Readme_ZH.md#run-backend)，在`9283`端口运行后端。
2. 访问<https://canvashelper2.web.app/canvashelper/>来配置你的CanvasHelper
3. 访问<https://canvashelper2.web.app/>预览结果
4. 使用[插件](https://github.com/linsyking/CanvasHelper2/blob/main/doc/Readme_ZH.md#部署到桌面)在桌面上部署Canvas Helper

## 开发流程

如果你想使用自己的前端或为这个项目做出贡献，你主要需要做3个步骤:

1. 运行后端
2. 运行`CanvasHelper2-conf`，在浏览器中配置CanvasHelper
3. 运行HTTP服务器来托管静态HTML文件(或开发自己的dashboard前端)

## 运行后端

首先，克隆这个仓库:

```bash
git clone https://github.com/linsyking/CanvasHelper2.git

cd CanvasHelper2
```

安装依赖项:

```bash
pip3 install -r requirements.txt
```

如果你不想改变任何设置(如CORS)，你可以直接运行以下代码:(如果你想使用我们的服务器上的前端，你必须使用`9283`端口)

```bash
uvicorn canvas_app:app --port 9283
```

开发者可能需要使用:

```bash
uvicorn canvas_app:app --reload
```

在脚本被修改时自动重新加载API。

如果你需要公开端口，你可以添加选项`--host 0.0.0.0`。

## 配置CanvasHelper

如果你想在我们的服务器上使用前端，请访问: [这里](https://canvashelper2.web.app/canvashelper/)。(网站未来可能会有变动)

如果你想在本地运行前端，请访问[CanvasHelper2-conf](https://github.com/linsyking/CanvasHelper2-conf)获取更多详细信息。

## 预览结果

如果你想在不托管HTML文件的情况下预览结果，你可以直接访问[这里](https://canvashelper2.web.app/)。

您可以使用任何您喜欢的http服务器来托管静态html文件。

示例dashboard前端位于<https://github.com/linsyking/CanvasHelper2-dashboard>

您可以克隆该存储库并通过

```bash
python3 -m http.server 9282
```

来托管这些文件。

现在，你可以访问<http://localhost:9282>页面查看结果。

## 部署到桌面

### Wallpaper Engine

订阅模板壁纸: <https://steamcommunity.com/sharedfiles/filedetails/?id=2913474561>

在本地启动后端后，它将重定向到[这里](https://canvashelper2.web.app/)。您也可以将其更改为本地前端。

要在启动时自动运行后端，您可以执行以下操作:

1. Win+R，输入“shell:startup”
2. 在打开的窗口中，创建一个名为canvashelper.vbs的文件。

其内容应该是这样的:

```vbs
Dim WinScriptHost
Set WinScriptHost = CreateObject("WScript.Shell")
WinScriptHost.Run Chr(34) & "C:\XXX\canvashelper.bat" & Chr(34), 0
Set WinScriptHost = Nothing
```

将`C:\XXX\ CanvasHelper. bat`替换为存放用于启动CanvasHelper的`bat`文件的路径。

**该bat脚本必须在C盘中**

3.创建包含以下内容的`C:\XXX\canvashelper.bat`文件:

```cmd
@echo off

d:
cd D:\Project\CanvasHelper2
uvicorn canvas_app:app --port 9283
```

将`d:`和`D:\Project\CanvasHelper2`替换为你自己的目录。

(如果你的克隆的仓库在C盘下，那么你不需要' d: '来进入D盘)

之后，系统将在启动时运行此脚本。

**注意:壁纸引擎中的一些功能不支持，包括滚动**

### KDE Wallpaper

1. 安装[wallpaper-engine-kde-plugin](https://github.com/catsout/wallpaper-engine-kde-plugin)。
2. 下载canvas wallpaper <https://steamcommunity.com/sharedfiles/filedetails/?id=2913474561>
3. 你应该能看到墙纸。
4. 添加一个自启动脚本来运行后端

**注: 同样不支持滚动**

结果:

![demo](https://user-images.githubusercontent.com/49303317/210978732-68cefd73-75df-4013-a7cb-2010f16ec7dd.png)

### KDE Widget

(另一个dashboard前端)

*To-Do*

## 常见问题解答

- CanvasHelper和CanvasHelper 2的区别是什么?

> CanvasHelper1是中心化的，而CanvasHelper 2不是。它完全是本地的，所以你不需要连接到我们的服务器来使用CanvasHelper。
> 此外，CanvasHelper2提供了一个方便的web界面来配置课程。
> CanvasHelper2将前端和后端分开，这样你就可以在任何操作系统/桌面环境下开发自己的dashboard前端。

- Canvas Helper后端，前端和dashboard之间的关系是什么?

> 后端提供了几个api供前端和dashboard调用;前端使用本地api来配置Canvas Helper。dashboard还调用本地后端来获取配置。

- 我一定要使用样本dashboard吗？

> 不一定。你可以开发你自己的dashboard前端。这个样本前端使用后端的HTML输出并在一个可拖拽的组建中展示。
