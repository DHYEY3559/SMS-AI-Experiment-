import requests
import json

API_KEY = "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"  # put your new OpenRouter key

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
