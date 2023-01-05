# Canvas Helper 2

New generation of Canvas Helper backend.

## Demo

Currently we have hosted a demo at [here](https://yydbxx.cn/test/canvashelper/). We made some small change to that API so that you cannot access the secret.

## Workflow

To see the result in the demo, you have to do mainly 3 steps.

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

If you don't want to change any settings (like CORS), you can directly run:

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

Goto [CanvasHelper2-conf](https://github.com/linsyking/CanvasHelper2-conf) for more details.

## Host static files

You can use any http server you like to host the static html file.

For example,

```bash
python3 -m http.server 9282 --directory ./public/
```

Now go to page <http://localhost:9282> to see the result!

## Use CanvasHelper in ...

### Wallpaper Engine

You will need to download a template wallpaper and edit the HTML to redirect to `http://localhost:9282`.

**Note: some features in wallpaper engine are not well-supported, including scrolling.**

### KDE

*TO-DO*

## FAQ

- What's the difference between CanvasHelper and CanvasHelper 2?

> CanvasHelper 1 is centralized while CanvasHelper 2 is not. It is completely local so you don't have to connect to our server to use CanvasHelper.
> Moreover, CanvasHelper 2 provides a handy web interface for configuring courses.
