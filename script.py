import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin, urlparse
import time

class IframeChainExtractor:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        self.visited_urls = set()
        
        # Known player domains (final destinations)
        self.player_domains = [
            'rereyano.ru',
            'player',
            'embed',
            'stream',
            'live',
            'video'
        ]
    
    def fetch_page(self, url):
        """Fetch a page and return BeautifulSoup object"""
        try:
            if url in self.visited_urls:
                return None
            
            self.visited_urls.add(url)
            
            response = requests.get(url, headers=self.headers, timeout=15, allow_redirects=True)
            response.raise_for_status()
            
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"  ✗ Error fetching {url}: {str(e)}")
            return None
    
    def extract_iframes(self, soup, base_url):
        """Extract all iframe URLs from a page"""
        if not soup:
            return []
        
        iframes = soup.find_all('iframe')
        iframe_urls = []
        
        for iframe in iframes:
            src = iframe.get('src') or iframe.get('data-src')
            if src:
                absolute_url = urljoin(base_url, src)
                iframe_urls.append(absolute_url)
        
        return iframe_urls
    
    def is_player_url(self, url):
        """Check if URL is likely a final player URL"""
        url_lower = url.lower()
        parsed = urlparse(url)
        
        # Check if it's a known player domain
        for domain in self.player_domains:
            if domain in parsed.netloc.lower() or domain in parsed.path.lower():
                return True
        
        return False
    
    def follow_iframe_chain(self, start_url, max_depth=5):
        """Follow iframe chain and return the final player URL"""
        current_url = start_url
        depth = 0
        last_valid_url = None
        
        while depth < max_depth:
            soup = self.fetch_page(current_url)
            
            if not soup:
                break
            
            iframe_urls = self.extract_iframes(soup, current_url)
            
            if not iframe_urls:
                return current_url
            
            last_valid_url = iframe_urls[0]
            
            if self.is_player_url(last_valid_url):
                return last_valid_url
            
            current_url = iframe_urls[0]
            depth += 1
            time.sleep(0.3)
        
        return last_valid_url
    
    def extract_all_events(self, home_url, limit=None):
        """Extract all events with titles, times, and player URLs"""
        print(f"Fetching main page: {home_url}\n")
        
        soup = self.fetch_page(home_url)
        if not soup:
            return {'error': 'Failed to fetch main page'}
        
        events = []
        
        # Find all list items with class 'toggle-submenu'
        event_items = soup.find_all('li', class_='toggle-submenu')
        
        for item in event_items:
            # Extract event info from the match-item div
            match_item = item.find('div', class_='match-item')
            if not match_item:
                continue
            
            info_div = match_item.find('div', class_='info')
            if not info_div:
                continue
            
            # Extract time
            time_elem = info_div.find('time')
            event_time = time_elem.get('datetime') if time_elem else None
            
            # Extract event title from span
            title_span = info_div.find('span')
            event_title = title_span.get_text(strip=True) if title_span else 'Unknown Event'
            
            # Get sport category from data-category attribute
            sport_category = item.get('data-category', 'Unknown')
            
            # Find all canal links within this event's submenu
            submenu = item.find('ul', class_='submenu')
            if submenu:
                canal_links = submenu.find_all('a', class_='submenu-item')
                
                for canal_link in canal_links:
                    canal_href = canal_link.get('href')
                    if not canal_href:
                        continue
                    
                    # Extract canal name from span inside the link
                    canal_span = canal_link.find('span')
                    canal_name = canal_span.get_text(strip=True) if canal_span else 'Unknown Canal'
                    
                    # Get absolute URL
                    canal_url = urljoin(home_url, canal_href)
                    
                    print(f"\n{'='*70}")
                    print(f"Event: {event_title}")
                    if event_time:
                        print(f"Time: {event_time}")
                    print(f"Sport: {sport_category}")
                    print(f"Canal: {canal_name}")
                    print(f"{'='*70}")
                    
                    # Follow to find final player URL
                    player_url = self.follow_iframe_chain(canal_url, max_depth=5)
                    
                    if player_url:
                        domain = urlparse(player_url).netloc
                        
                        event = {
                            'event_title': event_title,
                            'event_time': event_time,
                            'sport': sport_category,
                            'canal_name': canal_name,
                            'canal_url': canal_url,
                            'player_url': player_url,
                            'player_domain': domain
                        }
                        
                        events.append(event)
                        print(f"  ✓ Player: {player_url}")
                    else:
                        print(f"  ✗ No player URL found")
                    
                    # Limit if specified
                    if limit and len(events) >= limit:
                        print(f"\n⚠ Limiting to first {limit} events")
                        return {
                            'source_url': home_url,
                            'total_events': len(events),
                            'events': events
                        }
        
        return {
            'source_url': home_url,
            'total_events': len(events),
            'events': events
        }

def save_to_json(data, filename='player_urls.json'):
    """Save data to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Data saved to {filename}")

if __name__ == "__main__":
    target_url = "https://tarjetaroja.com.co/"
    
    print("="*70)
    print("TARJETA ROJA EVENT EXTRACTOR")
    print("="*70)
    
    extractor = IframeChainExtractor()
    data = extractor.extract_all_events(target_url, limit=100)
    
    if 'error' in data:
        print(f"\n✗ Error: {data['error']}")
    else:
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        print(f"Total events extracted: {data['total_events']}")
        
        # Group by domain
        domains = {}
        for event in data['events']:
            domain = event['player_domain']
            domains[domain] = domains.get(domain, 0) + 1
        
        print(f"\nPlayer domains found:")
        for domain, count in domains.items():
            print(f"  • {domain}: {count} events")
        
        print(f"\nSample Events:")
        for i, event in enumerate(data['events'][:5], 1):
            print(f"\n{i}. {event['event_title']}")
            if event['event_time']:
                print(f"   Time: {event['event_time']}")
            print(f"   Sport: {event['sport']}")
            print(f"   Canal: {event['canal_name']}")
            print(f"   Player: {event['player_url']}")
    
    save_to_json(data)
    print("\n✓ Done!")
