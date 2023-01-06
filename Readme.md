# Canvas Helper 2

New generation of Canvas Helper backend.

## Demo

You can go to [demo](https://yydbxx.cn/test/canvashelper/) to see the final result. That backend is hosted on our server but it didn't allow you to see the secrets.

## Requirements

- Python >= 3.10

## Workflow

If you only want to run the backend on your machine and use the frontend on our server, do the follwoing:

1. Follow [documentation](https://github.com/linsyking/CanvasHelper2#run-backend), run the backend at port `9283`
2. Go to <https://yydbxx.cn/canvashelper/> to configure your CanvasHelper
2. Go to <https://yydbxx.cn/canvashelper/dashboard> to see the final result

## Dev Workflow

If you want to setup frontend by yourself or contribute to this project, you have to do mainly 3 steps:

1. Run the backend
2. Run `CanvasHelper2-conf` and configure CanvasHelper in the browser
3. Run an HTTP server to host the static HTML files

## Run backend

First, clone this repository:

```bash
git clone https://github.com/linsyking/CanvasHelper2.git

cd CanvasHelper2
```

Install the dependencies:

```bash
pip3 install -r requirements.txt
```

If you don't want to change any settings (like CORS), you can directly run: (If you want to use frontend on our server, you must use `9283` port)

```bash
uvicorn canvas_app:app --port 9283
```

For development, you probably need to use:

```bash
uvicorn canvas_app:app --reload
```

to automatically reload the api when the script is modified.

If you need to expose the port, you can add option `--host 0.0.0.0`.

## Configure CanvasHelper

If you want to use the frontend on your server, go to: [here](https://yydbxx.cn/canvashelper/). (Site might be changed in the future)

Otherwise, go to [CanvasHelper2-conf](https://github.com/linsyking/CanvasHelper2-conf) for more details.

## Host static files

If you want to see the result without hosting HTML files, you can directly go to [here](https://yydbxx.cn/canvashelper/dashboard/).

You can use any http server you like to host the static html file.

For example,

```bash
python3 -m http.server 9282 --directory ./public/
```

Now go to page <http://localhost:9282> to see the result!

## Use CanvasHelper in ...

### Wallpaper Engine

Subscribe template wallpaper: <https://steamcommunity.com/sharedfiles/filedetails/?id=2913474561>.

After you started the backend locally, it will redirect to the [here](https://yydbxx.cn/canvashelper/dashboard/). You can also change it to your local frontend.

To start the backend on startup, you can do the following:

1. Win+R, type `shell:startup`
2. In the opened window, create a file called `canvashelper.cmd`

Its content should be like this:

```cmd
@echo off

d:
cd D:\Project\CanvasHelper2
uvicorn canvas_app:app --port 9283
```

Make sure you change the directory to yours! Here my folder is `D:\Project\CanvasHelper2`.

After that, your system will run this script on startup.

**Note: some features in wallpaper engine are not well-supported, including scrolling.**

### KDE

*TO-DO*

## FAQ

- What's the difference between CanvasHelper and CanvasHelper 2?

> CanvasHelper 1 is centralized while CanvasHelper 2 is not. It is completely local so you don't have to connect to our server to use CanvasHelper.
> Moreover, CanvasHelper 2 provides a handy web interface for configuring courses.

- What's the relationship between Canvas Helper backend, frontend, and dashboard?

> The backend provides several APIs for frontend and dashboard to call; frontend uses the local APIs to configure Canvas Helper. The dashboard also calls the local backend to get the configuration.
