import requests
import os

# Use your Bearer token here (not API key string directly)
GEMINI_BEARER_TOKEN = "YOUR_BEARER_TOKEN_HERE"

# Project number
PROJECT_NUMBER = "201487686622"

url = f"https://generativelanguage.googleapis.com/v1beta2/projects/{PROJECT_NUMBER}/locations/us-central1/models/text-bison-001:generate"

headers = {
    "Authorization": f"Bearer {GEMINI_BEARER_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "prompt": "Hello, test.",
    "temperature": 0.5,
    "maxOutputTokens": 10
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(response.text)