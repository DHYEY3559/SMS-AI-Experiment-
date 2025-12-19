import requests
import json

API_KEY = "sk-or-v1-94af01aXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # put your new OpenRouter key

res = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "mistralai/mistral-small-3.2-24b-instruct:free",
        "messages": [
            {"role": "system", "content": "Reply in 10 words or less."},
            {"role": "user", "content": "what is water"}
        ]
    }
)

print(res.status_code)
print(res.text)
