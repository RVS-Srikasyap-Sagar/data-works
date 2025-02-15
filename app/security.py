# app/security.py
from pathlib import Path

BLACKLISTED_COMMANDS = ["rm", "mv", "dd", ">", "|", "&", ";", "sudo"]

def validate_path(user_path: str, base_dir: Path) -> Path:
    safe_path = (base_dir / user_path).resolve()
    if not safe_path.is_relative_to(base_dir):
        raise PermissionError("Path traversal attempt")
    return safe_path

def sanitize_command(command: str) -> bool:
    return not any(
        cmd in command
        for cmd in BLACKLISTED_COMMANDS
    )
