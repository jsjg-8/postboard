from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

app = FastAPI(title="postboard")
LOG_FILE = Path("log.txt")
entries = []


@app.post("/")
async def receive(request: Request):
    body = await request.body()
    line = f"[{datetime.now().isoformat()}] {request.client.host} {body.decode()}"
    print(line, flush=True)
    entries.append(line)
    try:
        with LOG_FILE.open("a") as f:
            f.write(line + "\n")
    except OSError:
        pass
    return PlainTextResponse("OK\n")


@app.get("/")
async def view():
    return PlainTextResponse("\n".join(entries) + "\n" if entries else "(empty)\n")
