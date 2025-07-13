## 🧠 Reddit User Persona Generator

Generate detailed psychological user personas from Reddit profiles using scraped data and powerful LLM analysis.

---

### 📌 What It Does

* ✅ Takes a Reddit user profile link (e.g., `https://www.reddit.com/user/kojied/`)
* ✅ Scrapes **posts** and **comments** using the Reddit API
* ✅ Builds a detailed **user persona** using LLMs (via Together.ai)
* ✅ Outputs results in a clean `.txt` file with citations from their content

---

### 🚀 How to Use

1. **Clone this repo**

   ```bash
   git clone <your-repo-url>
   cd <repo-folder>
   ```

2. **Set up virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

3. **Add your API keys in a `.env` file**

   ```
   REDDIT_CLIENT_ID=your_reddit_client_id
   REDDIT_CLIENT_SECRET=your_reddit_client_secret
   TOGETHER_API_KEY=your_together_api_key
   ```

4. **Run with a Reddit profile link**

   ```bash
   python run_from_link.py https://www.reddit.com/user/AveragePotatoFarmer/
   ```

---

### 📂 Output

All results are saved inside the `output/` folder:

* `username_raw.csv` — Raw scraped data
* `persona_username.txt` — Final generated persona

---

### 🛠 Tech Stack

* 🐍 Python 3
* 📦 PRAW (Reddit API)
* 🌐 Together.ai (LLM API)
* 📄 Pandas, Requests, dotenv

---

### 📎 Sample Output Snippet

```
- Communication Style: Uses informal and sarcastic tone in comments.
- Personality Traits: Curious, opinionated, politically conscious.
- Interests: Technology, gaming, philosophy.
- Other Notes: Strong presence in niche subreddits like r/TrueAskReddit.
```

---

### 📬 Contact

Built as part of the AI/LLM Engineer Intern challenge by \[BeyondChats].

