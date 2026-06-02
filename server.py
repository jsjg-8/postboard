from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

app = FastAPI(title="postboard")
LOG_FILE = Path("log.txt")


@app.post("/")
async def receive(request: Request):
    body = await request.body()
    line = f"[{datetime.now().isoformat()}] {request.client.host} {body.decode()}"
    print(line, flush=True)
    with LOG_FILE.open("a") as f:
        f.write(line + "\n")
    return PlainTextResponse("OK\n")


@app.get("/")
async def view():
    if LOG_FILE.exists():
        return PlainTextResponse(LOG_FILE.read_text())
    return PlainTextResponse("(empty)\n")
