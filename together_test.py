import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_MODEL = "meta-llama/Llama-3-70b-chat-hf"  # You can change this later

def test_together():
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": TOGETHER_MODEL,
        "messages": [
            {"role": "user", "content": "Introduce yourself in one line."}
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)

    print("Status Code:", response.status_code)
    if response.status_code != 200:
        print("❌ Error:", response.text)
    else:
        data = response.json()
        print("✅ Response:", data["choices"][0]["message"]["content"])

if __name__ == "__main__":
    test_together()
