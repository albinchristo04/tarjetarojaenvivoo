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

def generate_rich_seo_text(event):
    title = event['event_title']
    time = event['event_time']
    sport = event['sport']
    
    # Templates for content generation - NEWS STYLE
    intros = [
        f"La jornada deportiva de hoy nos trae un interesante duelo entre <strong>{title}</strong>. Ambos equipos buscarán la victoria en este encuentro de {sport} que promete emociones fuertes.",
        f"Todo está listo para el enfrentamiento entre <strong>{title}</strong>. Los aficionados al {sport} tienen una cita ineludible hoy a las {time}.",
        f"Análisis previo del partido <strong>{title}</strong>. Descubre cómo llegan ambos conjuntos a este importante compromiso de {sport}."
    ]
    
    middles = [
        f"El partido está programado para las <strong>{time}</strong>. Se espera un gran ambiente para este choque de {sport}.",
        f"Las estadísticas sugieren un encuentro disputado. <strong>{title}</strong> es siempre un partido que atrae miradas.",
        f"A las {time} comenzará a rodar el balón. ¿Quién se llevará los puntos en este duelo de {sport}?"
    ]
    
    outros = [
        "Sigue toda la información y el minuto a minuto de este y otros eventos deportivos en nuestra sección de noticias.",
        "Mantente informado con las últimas novedades del {sport} y los resultados en tiempo real.",
        "No te pierdas los detalles de {title} y consulta la programación completa de la jornada."
    ]
    
    # Construct the text
    text = f"""
    <div class="seo-content" style="padding: 20px; color: #333; line-height: 1.8; font-family: Arial, sans-serif;">
        <h2>Noticias: {title} - Previa del Partido</h2>
        <p>{random.choice(intros)}</p>
        
        <h3>Horario y Detalles del Encuentro</h3>
        <p>El evento deportivo entre <strong>{title}</strong> está pactado para iniciar a las <strong>{time}</strong> (Hora Local). Este partido corresponde a la jornada actual de {sport}.</p>
        
        <h3>Actualidad de los Equipos</h3>
        <p>{random.choice(middles)}</p>
        <p>Ambos contendientes llegan con objetivos claros. El rendimiento en los últimos partidos será clave para definir el resultado de hoy.</p>
        
        <h3>¿Cómo seguir el partido {title}?</h3>
        <p>Para los seguidores que deseen estar al tanto de las incidencias, ofrecemos cobertura completa y enlaces a las transmisiones oficiales y autorizadas cuando están disponibles.</p>
        
        <p><strong>Ficha del Partido:</strong></p>
        <ul style="list-style-type: none; padding: 0;">
            <li>⚽ <strong>Partido:</strong> {title}</li>
            <li>🏆 <strong>Deporte:</strong> {sport}</li>
            <li>⏰ <strong>Hora:</strong> {time}</li>
            <li>📅 <strong>Estado:</strong> Por Jugar</li>
        </ul>
        
        <p>{random.choice(outros)}</p>
    </div>
    """
    return text

def format_post_content(event):
    channels_html = ""
    for i, c in enumerate(event['channels']):
        active_class = "active" if i == 0 else ""
        channels_html += f"""<button onclick="changeChannel('{c['player_url']}', this)" class="btn {active_class}">Opción {i+1}</button> """

    main_player_url = event['channels'][0]['player_url'] if event['channels'] else ""
    title = event['event_title']
    time = event['event_time']
    
    # Generate rich text
    rich_text = generate_rich_seo_text(event)

    # AdSense Code
    adsense_code = """
    <div style="margin: 10px 0; text-align: center;">
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7025462814384100" crossorigin="anonymous"></script>
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="ca-pub-7025462814384100"
             data-ad-slot="1754817794"
             data-ad-format="auto"
             data-full-width-responsive="true"></ins>
        <script>
             (adsbygoogle = window.adsbygoogle || []).push({});
        </script>
    </div>
    """

    # Social Buttons Styles
    btn_style = "width: 48%; margin: 1%; padding: 10px; border: none; border-radius: 5px; font-weight: bold; color: white; cursor: pointer; display: inline-block; text-align: center; text-decoration: none;"

    html = f"""
    <div class="card">
        <div class="card-header">📺 {title}</div>
        
        {adsense_code}

        <!-- JOIN BUTTONS -->
        <div style="padding: 10px; text-align: center;">
            <a href="https://t.me/footballhdlive247" target="_blank" style="{btn_style} background: #0088cc;">
                ✈️ UNIRSE TELEGRAM
            </a>
            <a href="https://chat.whatsapp.com/EQH5y4Rp2X151eFwE8dbxQ" target="_blank" style="{btn_style} background: #25D366;">
                📱 UNIRSE WHATSAPP
            </a>
        </div>

        {adsense_code}

        <div class="player-container" id="player-wrapper">
            <div class="player-shield" onclick="removeShield(this)">
                <div class="shield-msg">CLIC PARA VER TRANSMISIÓN</div>
            </div>
            <iframe id="main-player" src="{main_player_url}" allowfullscreen="true" scrolling="no"></iframe>
        </div>

        {adsense_code}

        <div class="btn-grid">
            {channels_html}
        </div>

        <!-- SHARE BUTTONS -->
        <div style="padding: 15px; text-align: center;">
            <p style="margin-bottom: 10px; font-weight: bold;">👇 COMPARTIR CON AMIGOS 👇</p>
            <button onclick="shareToTelegram('{title}', '{time}', window.location.href)" class="btn" style="{btn_style} background: #0088cc;">
                ✈️ COMPARTIR TELEGRAM
            </button>
            <a href="whatsapp://send?text=Ver {title} En Vivo: " onclick="this.href='whatsapp://send?text=Ver {title} En Vivo: ' + window.location.href" class="btn" style="{btn_style} background: #25D366;">
                📱 COMPARTIR WHATSAPP
            </a>
        </div>
        
        {adsense_code}
    </div>
    
    {rich_text}
    """
    return html

def create_post(service, event):
    # NEWS STYLE TITLE - NEUTRAL
    title = f"{event['event_title']} - Previa y Horario {event['sport']}"
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
            "labels": [event['sport'], "Partidos"],
            "status": "LIVE",
            "published": datetime.datetime.utcnow().isoformat("T") + "Z"
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
