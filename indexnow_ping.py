"""
IndexNow Bulk URL Submission for Bing
Submits all site URLs to Bing via IndexNow protocol for instant indexing.
Run after every build to ensure Bing crawls new/updated content immediately.
"""
import requests
import json
import os
import sys
from datetime import datetime

# Configuration
DOMAIN = "www.tarjetarojaenvivo.live"
INDEXNOW_KEY = "tarjetarojaenvivoseo2026key01"  # Must match the key file in web/dist/
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"

def get_all_urls():
    """Generate all URLs that should be indexed."""
    base = f"https://{DOMAIN}"
    
    urls = [
        # Priority 1.0 - Core pages
        f"{base}/",
        
        # Priority 1.0 - Brand hub pages
        f"{base}/rojadirecta/",
        f"{base}/tarjeta-roja/",
        f"{base}/tarjeta-roja-tv/",
        f"{base}/pirlotv/",
        f"{base}/tarjeta-roja-en-vivo/",
        f"{base}/roja-directa/",
        f"{base}/rojadirecta-tv/",
        f"{base}/roja-tv/",
        f"{base}/targeta-roja/",
        f"{base}/la-roja-directa/",
        f"{base}/rojadirecta-futbol/",
        f"{base}/pirlo-tv-tarjeta-roja/",
        f"{base}/roja-directa-en-vivo/",
        f"{base}/futbol-en-vivo-gratis/",
        f"{base}/rojadirecta-online/",
        f"{base}/futbol-libre/",
        f"{base}/futbol-en-vivo/",
        
        # Priority 0.9 - League pages
        f"{base}/champions-league-en-vivo/",
        f"{base}/la-liga-en-vivo/",
        f"{base}/premier-league-en-vivo/",
        f"{base}/copa-libertadores-en-vivo/",
        f"{base}/liga-mx-en-vivo/",
        f"{base}/nba-en-vivo/",
        f"{base}/futbol-argentino-en-vivo/",
        f"{base}/brasileirao-en-vivo/",
        f"{base}/liga-betplay-en-vivo/",
        f"{base}/liga-peru-en-vivo/",
        f"{base}/liga-chilena-en-vivo/",
        f"{base}/copa-sudamericana-en-vivo/",
        
        # Agenda pages
        f"{base}/agenda/futbol-en-vivo-hoy",
        f"{base}/agenda/futbol-en-vivo-manana",
        
        # Legal
        f"{base}/aviso-legal",
        f"{base}/contacto",
    ]
    
    # Add match pages from the API
    try:
        api_url = "https://sportsonline.ppvtv.top/api/matches.json"
        resp = requests.get(api_url, timeout=10)
        data = resp.json()
        matches = data.get('matches', [])
        
        import re
        def get_slug(text):
            text = text.lower()
            text = re.sub(r'[^a-z0-9]+', '-', text)
            return text.strip('-')
        
        for m in matches:
            title = m.get('title', '')
            if title:
                slug = get_slug(title)
                urls.append(f"{base}/partido/{slug}-en-vivo")
    except Exception as e:
        print(f"⚠️ Could not fetch matches for URL list: {e}")
    
    return urls


def submit_indexnow(urls):
    """Submit URLs to IndexNow API (Bing, Yandex, etc.)."""
    # IndexNow accepts up to 10,000 URLs per request
    payload = {
        "host": DOMAIN,
        "key": INDEXNOW_KEY,
        "keyLocation": f"https://{DOMAIN}/{INDEXNOW_KEY}.txt",
        "urlList": urls[:10000]
    }
    
    print(f"📡 Submitting {len(urls)} URLs to IndexNow...")
    print(f"   Key: {INDEXNOW_KEY}")
    print(f"   Endpoint: {INDEXNOW_ENDPOINT}")
    
    try:
        resp = requests.post(
            INDEXNOW_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            timeout=30
        )
        
        if resp.status_code in (200, 202):
            print(f"✅ IndexNow accepted! Status: {resp.status_code}")
            return True
        elif resp.status_code == 422:
            print(f"⚠️ IndexNow: Some URLs invalid. Status: {resp.status_code}")
            print(f"   Response: {resp.text[:200]}")
            return True  # Partial success
        else:
            print(f"❌ IndexNow rejected. Status: {resp.status_code}")
            print(f"   Response: {resp.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ IndexNow request failed: {e}")
        return False


def ping_bing_sitemap():
    """Ping Bing with the sitemap URL (legacy method, still works)."""
    sitemap_url = f"https://{DOMAIN}/sitemap.xml"
    ping_url = f"https://www.bing.com/ping?sitemap={sitemap_url}"
    
    print(f"📡 Pinging Bing sitemap: {sitemap_url}")
    try:
        resp = requests.get(ping_url, timeout=10)
        if resp.status_code == 200:
            print(f"✅ Bing sitemap ping successful!")
        else:
            print(f"⚠️ Bing sitemap ping status: {resp.status_code}")
    except Exception as e:
        print(f"❌ Bing sitemap ping failed: {e}")


def ping_google_sitemap():
    """Ping Google with the sitemap URL."""
    sitemap_url = f"https://{DOMAIN}/sitemap.xml"
    ping_url = f"https://www.google.com/ping?sitemap={sitemap_url}"
    
    print(f"📡 Pinging Google sitemap: {sitemap_url}")
    try:
        resp = requests.get(ping_url, timeout=10)
        print(f"   Google response: {resp.status_code}")
    except Exception as e:
        print(f"⚠️ Google sitemap ping failed: {e}")


def main():
    print(f"🔔 IndexNow Bulk Submission — {datetime.utcnow().isoformat()}Z")
    print(f"   Domain: {DOMAIN}")
    print()
    
    # 1. Get all URLs
    urls = get_all_urls()
    print(f"📋 Total URLs to submit: {len(urls)}")
    for u in urls[:5]:
        print(f"   • {u}")
    if len(urls) > 5:
        print(f"   ... and {len(urls) - 5} more")
    print()
    
    # 2. Submit to IndexNow (Bing + Yandex + others)
    submit_indexnow(urls)
    print()
    
    # 3. Ping Bing sitemap (backup)
    ping_bing_sitemap()
    print()
    
    # 4. Ping Google sitemap
    ping_google_sitemap()
    print()
    
    print("✅ All pings complete!")


if __name__ == "__main__":
    main()
