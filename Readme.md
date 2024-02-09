# Canvas Helper 2

[![build](https://github.com/linsyking/CanvasHelper2/actions/workflows/build.yml/badge.svg)](https://github.com/linsyking/CanvasHelper2/actions/workflows/build.yml)

New generation of Canvas Helper backend. Web-based, support Linux, Windows and MacOS.

[Chinese Translation](doc/Readme_ZH.md)

## Requirements

- Python >= 3.7

## Workflow

### Sharing public server for multiple users

If you want to use our server and use the frontend hosted on our website:

1.  Run `python3 canvas_app.py`, which will start the uvicorn server on server_ip:9283
2.  Open https://canvashelper.netlify.app/signup to sign up for an account. A popup window will show up to set the backend URL. Enter the backend URL in form of `https://backend.com/`
3.  For account registration, the following information is required:
    1.  A unique username
    2.  Password
    3.  Canvas LMS URL
    4.  Canvas access key
4.  When successfully signed up, you will be redirected to https://canvashelper.netlify.app/login for login.
5.  You will be kept logged in if you regularly open CanvasHelper dashboard. If you haven't open it for some time (by default, 1 day), you will have to login again for security reasons (The Canvas access key provides full control over your Canvas account, so there are effective security precautions to protect the key).
6.  Visit https://canvashelper.netlify.app/canvashelper to configure CanvasHelper and courses information
7.  CanvasHelper dashboard is ready on https://canvashelper.netlify.app/
8.  Deploy Canvas Helper on your desktop with [wiget](https://github.com/linsyking/CanvasHelper2/#use-canvashelper-in-)

### Running locally

If you want to run the backend on your machine and use the frontend hosted on our website:

1. Run `python3 canvas_app.py`, which will start the uvicorn server on localhost:9283
2. Open https://canvashelper.netlify.app/signup to sign up for an account. A popup window will show up to set the backend URL. Click `confirm` or close the popup window to use default settings
3. For account registration, the following information is required:
   1.  A username
   2.  Password
   3.  Canvas LMS URL
   4.  Canvas access key
4. When successfully signed up, you will be redirected to https://canvashelper.netlify.app/login for login.
5. You will be kept logged in if you regularly open CanvasHelper dashboard. If you haven't open it for some time (by default, 1 day), you will have to login again for security reasons. When running locally, expiration time of the auth tokens can be edited in global_config.py.
6. Visit https://canvashelper.netlify.app/canvashelper to configure CanvasHelper and courses information
7. CanvasHelper dashboard is ready on https://canvashelper.netlify.app/
8. Deploy Canvas Helper on your desktop with [wiget](https://github.com/linsyking/CanvasHelper2/#use-canvashelper-in-)

## Dev Workflow

If you want to setup frontend by yourself or contribute to this project, you have to do mainly 3 steps:

1. Run the backend
2. Run `CanvasHelper2-conf` and configure CanvasHelper in the browser
3. Run an HTTP server to host the static HTML files (or develop your own dashboard frontend)

## Run backend

First, clone this repository:

```bash
git clone https://github.com/linsyking/CanvasHelper2.git

cd CanvasHelper2
```

Then install the dependencies. It is recommended to use a virtual environment for installation:

```bash
python -m venv env # You may want to change `python` to `python3` or other python binaries
source env/bin/activate # You may want to change the activation script according to your shell
pip install -r requirements.txt
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

If you want to use the frontend on our server, go to: [here](https://canvashelper2.web.app/canvashelper/). (Site might be changed in the future)

Otherwise, go to [CanvasHelper2-conf](https://github.com/linsyking/CanvasHelper2-conf) for more details.

## Preview the result

If you want to see the result without hosting HTML files, you can directly go to [here](https://canvashelper2.web.app/).

You can use any http server you like to host the static html file.

The sample dashboard frontend is at <https://github.com/linsyking/CanvasHelper2-dashboard>.

You can clone that repository and host those files by

```bash
python3 -m http.server 9282
```

Now go to page <http://localhost:9282> to see the result!

## Use CanvasHelper in ...

### Wallpaper Engine

Subscribe template wallpaper: <https://steamcommunity.com/sharedfiles/filedetails/?id=2913474561>.

After you started the backend locally, it will redirect to the [here](https://canvashelper2.web.app/). You can also change it to your local frontend.

To start the backend on startup, you can do the following:

1. Win+R, type `shell:startup`
2. In the opened window, create a file called `canvashelper.vbs`

Its content should be like this:

```vbs
Dim WinScriptHost
Set WinScriptHost = CreateObject("WScript.Shell")
WinScriptHost.Run Chr(34) & "C:\XXX\canvashelper.bat" & Chr(34), 0
Set WinScriptHost = Nothing
```

Replace `C:\XXX\canvashelper.bat` with a better path where you store a `bat` file which is used to launch the CanvasHelper.

**That bat file must be in C drive.**

3. Create that `C:\XXX\canvashelper.bat` file with the following content:

```cmd
@echo off

d:
cd D:\Project\CanvasHelper2
uvicorn canvas_app:app --port 9283
```

Replace `d:` and `D:\Project\CanvasHelper2` with your own directory.

(If your clone directory is in C, then you don't need `d:` to enter drive D)

After that, your system will run this script on startup.

**Note: some features in wallpaper engine are not well-supported, including scrolling.**

### KDE Wallpaper

1. Install [wallpaper-engine-kde-plugin](https://github.com/catsout/wallpaper-engine-kde-plugin).
2. Download the canvas wallpaper <https://steamcommunity.com/sharedfiles/filedetails/?id=2913474561>.
3. You should be able to see the wallpaper.
4. Add a startup script to run the backend.

**Note: scrolling is also not supported.**

Result:

![demo](https://user-images.githubusercontent.com/49303317/210978732-68cefd73-75df-4013-a7cb-2010f16ec7dd.png)

### KDE Widget

(Another dashboard frontend)

*TO-DO*

## FAQ

- What's the difference between CanvasHelper and CanvasHelper 2?

> CanvasHelper 1 is centralized while CanvasHelper 2 is not. It is completely local so you don't have to connect to our server to use CanvasHelper.
> Moreover, CanvasHelper 2 provides a handy web interface for configuring courses.
> CanvasHelper 2 separates frontend and backend so that you can develop your own dashboard frontend on any operating system/desktop environment.

- What's the relationship between Canvas Helper backend, frontend, and dashboard?

> The backend provides several APIs for frontend and dashboard to call; frontend uses the local APIs to configure Canvas Helper. The dashboard also calls the local backend to get the configuration.

- Do I have to use the sample dashboard frontend?

> No. You can develop your own dashboard frontend. The sample dashboard frontend uses the HTML output from this backend and displays it in a draggable box.
