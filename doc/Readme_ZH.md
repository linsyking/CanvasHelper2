# Canvas Helper 2

[![build](https://github.com/linsyking/CanvasHelper2/actions/workflows/build.yml/badge.svg)](https://github.com/linsyking/CanvasHelper2/actions/workflows/build.yml)

新一代canvas helper后端。
基于网页，支持Windows, Macos, linux。

## 目录

- 要求
- 部署
- 开发

## 要求

- Python >= 3.7

## 部署

1. 运行后端
2. 打开前端，进行配置
3. 网页上查看效果

### 运行后端

首先，克隆本仓库：

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

对于开发者，你可能需要：

```bash
uvicorn canvas_app:app --reload
```

在修改脚本后来重新加载api

如果你想要公开端口，你可以增加选项`--host 0.0.0.0`。

### 配置CanvasHelper

如果你想使用我们的服务器，可以访问[here](https://canvashelper2.web.app/canvashelper/)。（网站位置未来可能会变动）

如果你想使用自己的前端，你可以参照[CanvasHelper2-conf](https://github.com/linsyking/CanvasHelper2-conf)来获取更多信息

#### 托管静态文件

如果你想在不托管HTML文件的前提下预览效果，你可以直接访问[here](https://canvashelper2.web.app/)。

你可以使用任意端口托管静态文件

一个dashboard样例在<https://github.com/linsyking/CanvasHelper2-dashboard>.

你可以克隆此仓库并使用：

```bash
python3 -m http.server 9282
```

来托管静态html文件，并在<http://localhost:9282>查看结果
