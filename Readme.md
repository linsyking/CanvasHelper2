# Canvas Helper 2

New generation of Canvas Helper backend.

## Run backend

```bash
uvicorn canvas_app:app --port 9283
```

For development, you'd probably need to use:

```bash
uvicorn canvas_app:app --reload
```

to automatically reload the api when the script is modified.

If you need to expose the port, you can add option `--host 0.0.0.0`.

## Run host

You can use any http server you like to host the static html file.

For example,

```bash
python3 -m http.server 9282 --directory ./public/
```

Now go to page <http://localhost:9282> to see the result!
