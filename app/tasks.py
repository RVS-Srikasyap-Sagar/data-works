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
# app/tasks.py (Add this function)
def install_and_run_uv(email: str):
    # Step 1: Install `uv` if not installed
    subprocess.run(["pip", "install", "uv"], check=True)
    
    # Step 2: Download and run the script
    script_url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
    script_path = BASE_DIR / "datagen.py"
    subprocess.run(["curl", "-o", str(script_path), script_url], check=True)
    
    # Step 3: Execute the script with the email argument
    subprocess.run(["python", str(script_path), email], check=True)

# app/tasks.py (Add this function)
def format_with_prettier(file_path: Path, version: str = "3.4.2"):
    subprocess.run(["npx", f"prettier@{version}", "--write", str(file_path)], check=True)

# app/tasks.py (Add this function)
def count_weekdays(file_path: Path, weekday_name: str, output_path: Path):
    from datetime import datetime

    weekday_map = {
        "monday": 0, "tuesday": 1, "wednesday": 2,
        "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6
    }
    weekday_num = weekday_map[weekday_name.lower()]

    with open(file_path) as f:
        dates = [line.strip() for line in f]

    count = sum(
        1 for date in dates
        if datetime.strptime(date, "%Y-%m-%d").weekday() == weekday_num
    )

    with open(output_path, "w") as f:
        f.write(str(count))

# app/tasks.py (Add this function)
import json

def sort_contacts(input_path: Path, output_path: Path):
    with open(input_path) as f:
        contacts = json.load(f)

    sorted_contacts = sorted(
        contacts,
        key=lambda c: (c["last_name"], c["first_name"])
    )

    with open(output_path, "w") as f:
        json.dump(sorted_contacts, f, indent=2)

# app/tasks.py (Add this function)
def extract_recent_logs(log_dir: Path, output_file: Path):
    log_files = sorted(
        log_dir.glob("*.log"),
        key=lambda f: f.stat().st_mtime,
        reverse=True
    )[:10]

    first_lines = []
    for log_file in log_files:
        with open(log_file) as f:
            first_lines.append(f.readline().strip())

    with open(output_file, "w") as f:
        f.write("\n".join(first_lines))

# app/tasks.py (Add this function)
import re

def create_markdown_index(doc_dir: Path, output_file: Path):
    index = {}
    
    for md_file in doc_dir.glob("*.md"):
        with open(md_file) as f:
            for line in f:
                if line.startswith("# "):  # H1 title
                    index[md_file.name] = line[2:].strip()
                    break

    with open(output_file, "w") as f:
        json.dump(index, f, indent=2)

# app/tasks.py (Add this function)
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

def find_similar_comments(input_file: Path, output_file: Path):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    with open(input_file) as f:
        comments = [line.strip() for line in f]

    embeddings = model.encode(comments)
    
    max_similarity = -1
    most_similar_pair = ("", "")
    
    for i in range(len(comments)):
        for j in range(i + 1, len(comments)):
            sim = cosine_similarity([embeddings[i]], [embeddings[j]])[0][0]
            if sim > max_similarity:
                max_similarity = sim
                most_similar_pair = (comments[i], comments[j])

    with open(output_file, "w") as f:
        f.write("\n".join(most_similar_pair))

# app/tasks.py (Add this function)
import sqlite3

def calculate_gold_sales(db_path: Path, output_file: Path):
    conn = sqlite3.connect(db_path)
    
    query = """
        SELECT SUM(units * price) AS total_sales
        FROM tickets
        WHERE type = 'Gold'
    """
    
    cursor = conn.execute(query)
    total_sales = cursor.fetchone()[0]
    
    with open(output_file, "w") as f:
        f.write(str(total_sales))
    
    conn.close()

