import os
import requests

GROQ_API_KEY = "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"  # Replace with your actual Groq key

def analyze_log_line(line):
    prompt = f"""
You are an AI trained to analyze log lines. For the given log entry, determine the type of log (e.g., ERROR, WARNING, INFO, DEBUG) and provide an explanation and resolution.

Log entry:
{line}

Response format:
Type: <Type of log (ERROR, WARNING, INFO, DEBUG)>
Definition: <What this log means, and why it’s important>
Resolution: <What a developer can do to resolve this issue or handle it>
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama3-70b-8192",  # Or the model you want to use on Groq
        "messages": [
            {"role": "system", "content": "You are a helpful log analysis assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",  # Groq's endpoint
        headers=headers,
        json=payload,
        timeout=30
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Groq API Error: {response.status_code} — {response.text}")
