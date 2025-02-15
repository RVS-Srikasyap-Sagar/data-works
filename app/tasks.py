# app/tasks.py
import json
import subprocess
from pathlib import Path
from .llm import LLMClient
from .security import sanitize_command, validate_path

BASE_DIR = Path("/data")

async def process_task(task_description: str):
    llm = LLMClient()
    response = await llm.parse_task(task_description)
    steps = json.loads(response)
    
    for step in steps:
        if step["action"] == "run_command":
            cmd = step["command"]
            if not sanitize_command(cmd):
                raise ValueError(f"Invalid command: {cmd}")
            subprocess.run(cmd, shell=True, check=True)
        
        elif step["action"] == "write_file":
            path = validate_path(step["path"], BASE_DIR)
            path.write_text(step["content"])
        
        elif step["action"] == "execute_script":
            script = step["script"]
            if not script.startswith("#!"):
                raise ValueError("Invalid script format")
            script_path = BASE_DIR / "temp_script.sh"
            script_path.write_text(script)
            subprocess.run(["sh", str(script_path)], check=True)
