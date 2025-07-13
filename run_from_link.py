import sys
import re
from reddit_scraper import scrape_user_data, save_to_csv
from persona_generator import load_user_data_from_csv, generate_persona

def extract_username_from_url(url):
    match = re.search(r"reddit\.com\/user\/([A-Za-z0-9_-]+)\/?", url)
    if not match:
        print("❌ Invalid Reddit profile URL.")
        return None
    return match.group(1)

def main():
    if len(sys.argv) < 2:
        print("❌ Usage: python run_from_link.py <reddit_user_profile_url>")
        return

    url = sys.argv[1]
    username = extract_username_from_url(url)

    if not username:
        return

    print(f"🚀 Generating persona for: u/{username}")

    try:
        print("🧹 Scraping Reddit data...")
        df = scrape_user_data(username)
        save_to_csv(df, username)
    except Exception as e:
        print(f"❌ Scraping failed: {e}")
        return

    try:
        print("🧠 Generating persona using LLM...")
        content = load_user_data_from_csv(username)
        generate_persona(content, username)
    except Exception as e:
        print(f"❌ Persona generation failed: {e}")
        return

    print(f"✅ Done! Persona saved in output/persona_{username}.txt")

if __name__ == "__main__":
    main()
