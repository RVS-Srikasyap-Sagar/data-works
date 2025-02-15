# app/llm.py
import os
import aiohttp
from .config import settings

PROMPT_TEMPLATE = """
Convert this task into executable steps in JSON format:
{task}

Output format:
{{
  "steps": [
    {{
      "action": "run_command" | "write_file" | "execute_script",
      "command": "command to execute" (if action=run_command),
      "path": "output path" (if action=write_file),
      "content": "file content" (if action=write_file),
      "script": "script content" (if action=execute_script)
    }}
  ]
}}
"""

class LLMClient:
    def __init__(self):
        self.token = settings.ai_proxy_token
        self.base_url = "https://api.ai-proxy.io/v1"
    
    async def parse_task(self, task: str):
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "gpt-4o-mini",
                "messages": [{
                    "role": "user",
                    "content": PROMPT_TEMPLATE.format(task=task)
                }],
                "max_tokens": 1000
            }
            
            async with session.post(
                f"{self.base_url}/chat/completions",
                json=data,
                headers=headers
            ) as resp:
                result = await resp.json()
                return result["choices"][0]["message"]["content"]
