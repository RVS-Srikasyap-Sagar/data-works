# app/main.py
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse
from pathlib import Path
import subprocess
from typing import Optional
import os
from .tasks import process_task
from .security import validate_path
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
BASE_DIR = Path("/data")

@app.post("/run")
async def run_task(task: str = Query(..., min_length=1)):
    try:
        await process_task(task)
        return {"status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/read", response_class=PlainTextResponse)
async def read_file(path: str):
    try:
        safe_path = validate_path(path, BASE_DIR)
        if not safe_path.exists():
            raise HTTPException(status_code=404)
        return safe_path.read_text()
    except PermissionError:
        raise HTTPException(status_code=403)
