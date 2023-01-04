# Canvas Helper 2

New generation of Canvas Helper backend.

## Usage

```bash
uvicorn canvas_app:app --host 0.0.0.0 --port 9283
```

For development, you'd probably need to use:

```bash
uvicorn canvas_app:app --reload
```

to automatically reload the api when the script is modified.
