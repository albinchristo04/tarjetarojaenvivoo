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
        
        # Find all list items with class matching sports (NBA, etc.)
        event_items = soup.find_all('li', class_=True)
        
        for item in event_items:
            # Skip subitem entries
            if 'subitem' in ' '.join(item.get('class', [])):
                continue
            
            # Get the main event link (the one with #)
            main_link = item.find('a', href='#')
            if not main_link:
                continue
            
            # Extract event title and time
            event_title = main_link.get_text(strip=True)
            
            # Extract time from span with class 't'
            time_span = main_link.find('span', class_='t')
            event_time = time_span.get_text(strip=True) if time_span else None
            
            # Remove time from title if present
            if event_time and event_time in event_title:
                event_title = event_title.replace(event_time, '').strip()
            
            # Get sport category
            sport_category = ' '.join(item.get('class', []))
            
            # Find all canal links within this event's submenu
            submenu = item.find('ul')
            if submenu:
                canal_links = submenu.find_all('a', href=True)
                
                for canal_link in canal_links:
                    canal_href = canal_link.get('href')
                    canal_name = canal_link.get_text(strip=True)
                    canal_url = urljoin(home_url, canal_href)
                    
                    # Only process if it's a canal-XX.php link or similar
                    if re.search(r'canal-?\d+\.php', canal_href, re.IGNORECASE) or 'capo-deportes' in canal_href:
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
    target_url = "https://www.tarjetarojaenvivo.club/home.php"
    
    print("="*70)
    print("EVENT EXTRACTOR WITH TITLES & TIMES")
    print("="*70)
    
    extractor = IframeChainExtractor()
    data = extractor.extract_all_events(target_url, limit=15)
    
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
