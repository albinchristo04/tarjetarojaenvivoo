import os
import json
import datetime
import requests
import random
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Configuration
BLOG_ID = "3632798063533467949"  # User must replace this
JSON_URL = "https://raw.githubusercontent.com/albinchristo04/tarjetarojaenvivoo/refs/heads/main/results/player_urls_latest.json"
SCOPES = ['https://www.googleapis.com/auth/blogger']
TOKEN_FILE = 'token.pickle'
CREDENTIALS_FILE = 'client_secrets.json'

def get_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return build('blogger', 'v3', credentials=creds)

def fetch_matches():
    try:
        response = requests.get(JSON_URL)
        response.raise_for_status()
        return response.json().get('events', [])
    except Exception as e:
        print(f"Error fetching matches: {e}")
        return []

def format_post_content(event):
    # Replicating the HTML structure from the original React/Python generator
    # This content goes into the post body
    
    channels_html = ""
    for i, c in enumerate(event['channels']):
        active_class = "active" if i == 0 else ""
        channels_html += f"""<button onclick="changeChannel('{c['player_url']}', this)" class="btn {active_class}">{c['canal_name']}</button> """

    # Main player is the first channel
    main_player_url = event['channels'][0]['player_url'] if event['channels'] else ""
    
    title = event['event_title']
    time = event['event_time']
    sport = event['sport']
    
    # SEO Content (Simplified for Blogger)
    seo_text = f"""
    <div class="seo-section">
        <h2>Cómo ver {title} en vivo</h2>
        <p>Disfruta del partido <strong>{title}</strong> en vivo y en directo. Transmisión oficial por <strong>Tarjeta Roja</strong> y <strong>Rojadirecta</strong>.</p>
        <p>Hora del partido: {time}</p>
        <p>Competición: {sport}</p>
    </div>
    """

    html = f"""
    <div class="card">
        <div class="card-header">🔴 EN VIVO: {title}</div>
        <div class="player-container" id="player-wrapper">
            <div class="player-shield" onclick="removeShield(this)">
                <div class="shield-msg">CLIC PARA VER EL PARTIDO</div>
            </div>
            <iframe id="main-player" src="{main_player_url}" allowfullscreen="true" scrolling="no"></iframe>
        </div>
        <div class="btn-grid">
            {channels_html}
        </div>
        <div style="padding: 15px; text-align: center;">
            <button onclick="shareToTelegram('{title}', '{time}', window.location.href)" class="btn" style="background: #0088cc; width: 100%; max-width: 300px;">
                ✈️ COMPARTIR EN TELEGRAM
            </button>
        </div>
    </div>
    {seo_text}
    """
    return html

def create_post(service, event):
    title = f"[{event['event_time']}] {event['event_title']}"
    content = format_post_content(event)
    
    # Check if post already exists (simple check by title)
    # In a real scenario, you might want to store IDs or use labels
    try:
        # Use search() instead of list() for query parameter 'q'
        search = service.posts().search(blogId=BLOG_ID, q=title).execute()
        if 'items' in search and len(search['items']) > 0:
            # Double check exact title match to be safe
            for item in search['items']:
                if item['title'] == title:
                    print(f"⚠️ Post already exists: {title}")
                    return False # Skip
            
        body = {
            "kind": "blogger#post",
            "blog": {"id": BLOG_ID},
            "title": title,
            "content": content,
            "labels": [event['sport'], "Rojadirecta", "En Vivo"],
            "status": "LIVE"
        }
        
        posts = service.posts().insert(blogId=BLOG_ID, body=body).execute()
        print(f"✅ Created post: {title}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating post {title}: {e}")
        return False

def main():
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"❌ Error: {CREDENTIALS_FILE} not found. Please download it from Google Cloud Console.")
        return

    service = get_service()
    matches = fetch_matches()
    
    print(f"Found {len(matches)} matches.")
    
    # Group matches by title/time to avoid duplicates if the JSON has multiple channels as separate entries
    # The original script grouped them. Let's do a simple grouping.
    grouped = {}
    for e in matches:
        key = f"{e['event_time']}-{e['event_title']}"
        if key not in grouped:
            grouped[key] = {
                "event_title": e['event_title'],
                "event_time": e['event_time'],
                "sport": e['sport'],
                "channels": []
            }
        grouped[key]['channels'].append(e)
    
    # Limit to 5 posts per run to avoid rate limits (User Request)
    posts_limit = 5
    print(f"🎯 Target for this run: {posts_limit} new posts.")
    
    posts_created = 0
    
    for key, event in grouped.items():
        if posts_created >= posts_limit:
            print("🛑 Reached post limit for this run. Exiting.")
            break
            
        if create_post(service, event):
            posts_created += 1
            # Add a small delay between posts to be safer and avoid rate limits
            import time
            time.sleep(random.uniform(5, 10))
            
    print(f"✅ Run complete. Created {posts_created} new posts.")

if __name__ == "__main__":
    main()
