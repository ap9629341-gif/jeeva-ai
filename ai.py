user_memory = {}
import requests
import json

def stream_ai_reply(message, language="Hindi", role="friend", user="local"):
    prompt = f"""
You are Jeeva AI.
Language: {language}
Role: {role}

User: {message}
Reply naturally and helpfully.
"""

    with requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": True
        },
        stream=True,
        timeout=120
    ) as r:
        for line in r.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                token = data.get("response", "")
                if token:
                    yield token
