import os
import sys
import pandas as pd
import requests
from dotenv import load_dotenv
from utils import chunk_text

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_MODEL = "meta-llama/Llama-3-70b-chat-hf"

def load_user_data_from_csv(username):
    path = f"output/{username}_raw.csv"
    if not os.path.exists(path):
        print(f"❌ CSV not found at: {path}")
        return ""

    df = pd.read_csv(path)

    content = ""

    for _, row in df.iterrows():
        # Safely extract fields with fallback
        post_type = row.get('type', '')
        subreddit = row.get('subreddit', '')
        title = row.get('title', '')
        body = row.get('body', '')
        post_id = row.get('id', '')
        link = row.get('link', '')

        if post_type == 'post':
            content += (
                f"[Post in r/{subreddit}]\n"
                f"Title: {title}\n"
                f"Body: {body}\n\n"
            )
        elif post_type == 'comment':
            content += (
                f"[Comment in r/{subreddit}]\n"
                f"{body}\n"
            )
            if post_id or link:
                content += f"(ID: {post_id})"
                if link:
                    content += f" | Link: {link}"
                content += "\n\n"
            else:
                content += "\n"

    return content

def generate_persona(content, username_suffix=""):
    if not content.strip():
        print("⚠️ No content found to analyze.")
        return ""

    prompt = f"""
You are a professional psychological profiler. Based on the following Reddit user's posts and comments, generate a detailed user persona. Use bullet points in the following format:

- Communication Style
- Personality Traits & Attitudes
- Interests & Hobbies
- Political Ideology
- Values and Beliefs
- Other Notes

Text:
\"\"\" 
{content}
\"\"\"
"""

    print("📤 Sending prompt to Together.ai...")

    response = requests.post(
        "https://api.together.xyz/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": TOGETHER_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1024,
            "temperature": 0.7
        }
    )

    print("🔄 Status Code:", response.status_code)

    if response.status_code != 200:
        print("❌ Error:", response.text)
        return ""

    try:
        output = response.json()["choices"][0]["message"]["content"]
        return output
    except Exception as e:
        print("❌ Parsing error:", e)
        print(response.text)
        return ""


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python persona_generator.py <reddit_username>")
        sys.exit(1)

    username = sys.argv[1]
    content = load_user_data_from_csv(username)

    # Split content into token-safe chunks
    chunks = chunk_text(content, max_tokens=3000)
    print(f"🧩 Splitting content into {len(chunks)} chunks...")

    final_profile = ""
    for i, chunk in enumerate(chunks):
        print(f"🔹 Processing chunk {i+1}/{len(chunks)}")
        partial = generate_persona(chunk, f"{username}_chunk{i+1}")
        final_profile += f"\n\n-----\nCHUNK {i+1}:\n{partial}"

    # Save the final merged persona
    os.makedirs("output", exist_ok=True)
    final_path = f"output/persona_{username}_final.txt"
    with open(final_path, "w", encoding="utf-8") as f:
        f.write(final_profile)

    print(f"✅ Final persona saved to: {final_path}")
