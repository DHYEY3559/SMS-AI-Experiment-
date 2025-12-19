# main.py — Flask Server to Handle SMS & Auto-Reply via TextBee (No Rate Limit)

import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

app = Flask(__name__)

# === CONFIG ===
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
TEXTBEE_API_KEY = os.getenv("TEXTBEE_API_KEY")


def ask_openrouter(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    system_prompt = (
        "Reply in 100 characters or less. "
        "Be concise. Avoid phrases like 'As an AI'."
    )

    data = {
        "model": "google/gemma-3-4b-it:free",  # ✅ Gemma 3 model
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }

    r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]



@app.route("/sms-webhook", methods=["POST"])
def sms_webhook():
    data = request.get_json() or request.form
    sender = data.get("from")
    message = data.get("message")

    if not sender or not message:
        return "Missing fields", 400

    print(f"[ACCEPTED] {sender}")

    if not message.lower().startswith("dhyey:"):
        print(f"[IGNORED] {message}")
        return "Ignored", 200

    prompt = message.split("dhyey:", 1)[1].strip()
    print(f"[ASK] {sender}: {prompt}")

    try:
        reply = ask_openrouter(prompt).strip()[:100]
        print(f"[REPLY] {reply}")

        # Clean number for SMS sending
        clean_sender = sender.strip().replace(" ", "").replace("\u202A", "").replace("\u200E", "")

        # Send SMS via TextBee API
        DEVICE_ID = os.getenv("TEXTBEE_DEVICE_ID")  # Add this to your .env too

        # Send SMS via TextBee API
        res = requests.post(f"https://api.textbee.dev/api/v1/gateway/devices/{DEVICE_ID}/send-sms", headers={
            "x-api-key": TEXTBEE_API_KEY,
            "Content-Type": "application/json"
        }, json={
            "recipients": [clean_sender],
            "message": reply
        })


        print(f"[FORWARDED] Status: {res.status_code}, Response: {res.text}")
        return jsonify({"reply": reply}), 200

    except Exception as e:
        print(f"[ERROR] {e}")
        return "Error", 500


@app.route("/", methods=["GET"])
def home():
    return "✅ Jarvis Flask Server running."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
