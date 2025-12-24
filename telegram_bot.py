import os
import json
import requests
from datetime import datetime, timedelta

# Configuration
JSON_URL = "https://raw.githubusercontent.com/albinchristo04/tarjetarojaenvivoo/refs/heads/main/results/player_urls_latest.json"
STATE_FILE = "telegram_sent_posts.json"
DOMAIN = "https://www.tarjetarojaenvivo.live"

# Environment Variables (to be set in GitHub Secrets)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

def load_sent_posts():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_sent_posts(sent_posts):
    # Keep only last 100 posts to avoid file growth
    with open(STATE_FILE, 'w') as f:
        json.dump(sent_posts[-100:], f)

def send_telegram_message(text):
    if not BOT_TOKEN or not CHANNEL_ID:
        print("❌ Telegram credentials missing. Skipping post.")
        return False
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"❌ Error sending Telegram message: {e}")
        return False

def run_telegram_bot():
    print("🤖 Agent 16: Running Telegram Auto-Post Bot...")
    
    if not BOT_TOKEN or not CHANNEL_ID:
        print("⚠️ TELEGRAM_BOT_TOKEN or TELEGRAM_CHANNEL_ID not set. Running in DRY-RUN mode.")
    
    try:
        response = requests.get(JSON_URL)
        data = response.json()
    except Exception as e:
        print(f"❌ Error fetching JSON: {e}")
        return

    sent_posts = load_sent_posts()
    events = data.get('events', [])
    
    # Group by title and time to avoid duplicate channel posts for same match
    unique_matches = {}
    for e in events:
        match_id = f"{e['event_title']}_{e['event_time']}"
        if match_id not in unique_matches:
            unique_matches[match_id] = e

    posts_made = 0
    for match_id, e in unique_matches.items():
        if match_id in sent_posts:
            continue
            
        # Format URL (Slug logic must match generate_static.py)
        slug = e['event_title'].lower()
        slug = "".join([c if c.isalnum() else "-" for c in slug])
        slug = "-".join([s for s in slug.split("-") if s])
        match_url = f"{DOMAIN}/partido/{slug}-en-vivo"
        
        # Prepare Message
        message = (
            f"⚽ <b>{e['event_title']}</b>\n"
            f"⏰ {e['event_time']}\n"
            f"📺 Ver en vivo:\n"
            f"{match_url}\n\n"
            f"#tarjetaroja #rojadirecta #futbolenvivo #tarjetarojatv"
        )
        
        if BOT_TOKEN and CHANNEL_ID:
            if send_telegram_message(message):
                sent_posts.append(match_id)
                posts_made += 1
                print(f"✅ Posted: {e['event_title']}")
        else:
            # Dry run output
            print(f"--- DRY RUN POST ---\n{message}\n--------------------")
            sent_posts.append(match_id) # Mark as sent in dry run too for simulation
            posts_made += 1

    save_sent_posts(sent_posts)
    print(f"🏁 Telegram Bot finished. New posts: {posts_made}")

if __name__ == "__main__":
    run_telegram_bot()
