import praw
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()  # Load Reddit credentials from .env file

def get_reddit_client():
    return praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent="RedditPersonaApp by /u/yourusername"
    )
def scrape_user_data(username, limit=100):
    reddit = get_reddit_client()
    user = reddit.redditor(username)

    posts, comments = [], []

    print(f"🔍 Scraping data for u/{username}...")

    # Fetch user posts
    for i, post in enumerate(user.submissions.new(limit=limit)):
        posts.append({
            'id': f'post_{i}',
            'type': 'post',
            'subreddit': post.subreddit.display_name,
            'title': post.title,
            'body': post.selftext,
            'score': post.score,
            'link': f"https://www.reddit.com{post.permalink}"
        })

    # Fetch user comments
    for i, comment in enumerate(user.comments.new(limit=limit)):
        comments.append({
            'id': f'comment_{i}',
            'type': 'comment',
            'subreddit': comment.subreddit.display_name,
            'body': comment.body,
            'score': comment.score,
            'link': f"https://www.reddit.com{comment.permalink}"
        })

    df = pd.DataFrame(posts + comments)
    print(f"✅ Scraped {len(posts)} posts and {len(comments)} comments.")
    return df

def save_to_csv(df, username):
    os.makedirs("output", exist_ok=True)
    path = f"output/{username}_raw.csv"
    df.to_csv(path, index=False)
    print(f"📁 Saved raw data to {path}")

# For testing
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("❌ Usage: python reddit_scraper.py <reddit_username>")
        exit(1)
    username = sys.argv[1]
    df = scrape_user_data(username)
    save_to_csv(df, username)
