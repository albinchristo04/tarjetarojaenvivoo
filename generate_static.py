import json
import os
import re
import requests
from datetime import datetime

# Configuration
JSON_URL = "https://raw.githubusercontent.com/albinchristo04/tarjetarojaenvivoo/refs/heads/main/results/player_urls_latest.json"
OUTPUT_DIR = "static_site"
DOMAIN = "https://www.tarjetarojaenvivo.live"

# Ensure directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "partido"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "categoria"), exist_ok=True)

def get_slug(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def get_template(title, description, canonical, content, schema=""):
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical}">
    <link rel="icon" href="/favicon.ico">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:type" content="website">
    
    <style>
        :root {{ --red: #d32f2f; --dark: #1a1a1a; --light: #f4f4f4; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 0; background: #000; color: #fff; line-height: 1.6; }}
        header {{ background: var(--red); padding: 15px; text-align: center; border-bottom: 3px solid #fff; }}
        header h1 {{ margin: 0; font-size: 24px; text-transform: uppercase; }}
        nav {{ background: #333; padding: 10px; text-align: center; }}
        nav a {{ color: #fff; margin: 0 15px; text-decoration: none; font-weight: bold; font-size: 14px; }}
        nav a:hover {{ color: #ffcc00; }}
        .container {{ max-width: 1000px; margin: 20px auto; padding: 0 15px; }}
        .card {{ background: #fff; color: #333; border-radius: 5px; overflow: hidden; margin-bottom: 20px; }}
        .card-header {{ background: #333; color: #ffcc00; padding: 10px; font-weight: bold; text-align: center; }}
        .event-row {{ display: flex; align-items: center; padding: 12px; border-bottom: 1px solid #eee; text-decoration: none; color: inherit; transition: background 0.2s; }}
        .event-row:hover {{ background: #f9f9f9; }}
        .event-time {{ font-weight: bold; background: #eee; padding: 2px 8px; border-radius: 3px; margin-right: 15px; min-width: 50px; text-align: center; }}
        .event-sport-icon {{ margin-right: 10px; color: var(--red); font-size: 18px; }}
        .event-title {{ flex-grow: 1; font-weight: bold; }}
        .player-container {{ position: relative; padding-top: 56.25%; background: #000; }}
        .player-container iframe {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; }}
        .btn-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 10px; padding: 20px; background: #1a1a1a; }}
        .btn {{ background: var(--red); color: #fff; padding: 10px; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; text-decoration: none; text-align: center; }}
        .seo-section {{ background: #fff; color: #333; padding: 25px; border-radius: 5px; margin-top: 20px; }}
        footer {{ background: var(--red); color: #fff; text-align: center; padding: 20px; margin-top: 40px; font-size: 13px; }}
        @media (max-width: 600px) {{ .event-row {{ flex-wrap: wrap; }} .event-title {{ width: 100%; margin-top: 10px; }} }}
    </style>
    {schema}
</head>
<body>
    <header>
        <h1>Tarjeta Roja En Vivo</h1>
    </header>
    <nav>
        <a href="/">PROGRAMACIÓN</a>
        <a href="/categoria/futbol-en-vivo">FÚTBOL</a>
        <a href="/categoria/nba-en-vivo">NBA</a>
        <a href="/aviso-legal">AVISO LEGAL</a>
        <a href="/contacto">CONTACTO</a>
    </nav>
    <div class="container">
        {content}
    </div>
    <footer>
        <p>TARJETA ROJA | Rojadirecta TV | Pirlo TV | Deportes En Vivo Online Gratis</p>
        <p>&copy; 2025 tarjetarojaenvivo.live - Todos los derechos reservados</p>
    </footer>
</body>
</html>"""

def generate_site():
    print("Fetching JSON data...")
    try:
        data = requests.get(JSON_URL).json()
    except Exception as e:
        print(f"Error fetching JSON: {e}")
        return

    events = data['events']
    
    # Group events by title and time
    grouped = {}
    for e in events:
        key = f"{e['event_time']}-{e['event_title']}"
        if key not in grouped:
            grouped[key] = {
                "title": e['event_title'],
                "time": e['event_time'],
                "sport": e['sport'],
                "slug": get_slug(e['event_title']),
                "channels": []
            }
        grouped[key]['channels'].append(e)

    # 1. Generate Homepage
    print("Generating Homepage...")
    hp_content = '<div class="card"><div class="card-header">PROGRAMACIÓN DE HOY</div>'
    for key in sorted(grouped.keys()):
        e = grouped[key]
        hp_content += f"""
        <a href="/partido/{e['slug']}-en-vivo" class="event-row">
            <div class="event-time">{e['time']}</div>
            <div class="event-sport-icon">📺</div>
            <div class="event-title">{e['title']}</div>
            <div style="color: var(--red); font-weight: bold;">VER AHORA &raquo;</div>
        </a>"""
    hp_content += '</div>'
    
    hp_content += """
    <div class="seo-section">
        <h2>Ver Fútbol En Vivo en Tarjeta Roja</h2>
        <p>Bienvenido a <strong>Tarjeta Roja En Vivo</strong>, la mejor alternativa a <strong>Rojadirecta</strong> y <strong>Pirlo TV</strong>. Aquí podrás ver todos los partidos de fútbol de hoy, NBA, F1 y MotoGP totalmente gratis y en alta definición.</p>
        <h3>Rojadirecta TV y Tarjeta Roja Directa</h3>
        <p>Nuestra plataforma recopila los mejores enlaces de <strong>Rojadirecta TV</strong> para que no te pierdas ni un segundo de la acción. Si buscas ver fútbol online gratis, este es tu sitio de confianza.</p>
    </div>"""
    
    hp_html = get_template(
        "Tarjeta Roja En Vivo | Rojadirecta TV | Fútbol Gratis Online",
        "Ver fútbol en VIVO en Tarjeta Roja. Agenda de hoy: Real Madrid, Barcelona, NBA, F1. La mejor alternativa a Rojadirecta y Pirlo TV. ¡Entra YA!",
        DOMAIN + "/",
        hp_content
    )
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(hp_html)

    # 2. Generate Match Pages
    print("Generating Match Pages...")
    for key, e in grouped.items():
        match_title = f"Ver {e['title']} EN VIVO Online Gratis | Tarjeta Roja"
        match_desc = f"Disfruta del partido {e['title']} en vivo y gratis. Enlaces de Rojadirecta, Pirlo TV y Tarjeta Roja para ver deportes online hoy."
        match_url = f"{DOMAIN}/partido/{e['slug']}-en-vivo"
        
        # Schema
        schema = f"""
        <script type="application/ld+json">
        {{
            "@context": "https://schema.org",
            "@type": "SportsEvent",
            "name": "{e['title']}",
            "description": "{match_desc}",
            "startDate": "{datetime.now().strftime('%Y-%m-%d')}T{e['time']}",
            "sport": "{e['sport']}",
            "location": {{ "@type": "Place", "name": "Online" }},
            "offers": {{
                "@type": "Offer",
                "url": "{match_url}",
                "price": "0",
                "priceCurrency": "USD",
                "availability": "https://schema.org/InStock"
            }}
        }}
        </script>"""
        
        match_content = f"""
        <div class="card">
            <div class="card-header">{e['title']} - {e['time']}</div>
            <div class="player-container">
                <iframe src="{e['channels'][0]['player_url']}" allowfullscreen scrolling="no"></iframe>
            </div>
            <div class="btn-grid">
                {" ".join([f'<a href="{c["player_url"]}" class="btn">{c["canal_name"]}</a>' for c in e['channels']])}
            </div>
        </div>
        <div class="seo-section">
            <h2>Cómo ver {e['title']} en directo</h2>
            <p>Sigue la transmisión en vivo de <strong>{e['title']}</strong> a través de nuestros canales gratuitos. En <strong>Tarjeta Roja</strong> ofrecemos la mejor calidad de streaming para eventos de {e['sport']}.</p>
            <p>Si el reproductor no carga, intenta cambiar de canal usando los botones superiores. Recuerda que somos la mejor opción para ver <strong>Rojadirecta en vivo</strong>.</p>
        </div>"""
        
        match_html = get_template(match_title, match_desc, match_url, match_content, schema)
        
        # Save file
        file_path = os.path.join(OUTPUT_DIR, "partido", f"{e['slug']}-en-vivo.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(match_html)

    # 3. Generate Category Pages
    print("Generating Category Pages...")
    categories = {
        "futbol-en-vivo": "Fútbol En Vivo",
        "nba-en-vivo": "NBA En Vivo",
        "tarjeta-roja-tv": "Tarjeta Roja TV"
    }
    
    for slug, name in categories.items():
        cat_title = f"{name} | Ver Deportes Online Gratis | Tarjeta Roja"
        cat_desc = f"Toda la programación de {name} en directo. Ver Rojadirecta, Pirlo TV y los mejores eventos deportivos hoy gratis."
        cat_url = f"{DOMAIN}/categoria/{slug}"
        
        cat_content = f'<div class="card"><div class="card-header">{name.upper()} - AGENDA</div>'
        # Filter events for this category (simplified logic)
        for key in sorted(grouped.keys()):
            e = grouped[key]
            if slug == "futbol-en-vivo" and e['sport'].lower() != "nba":
                pass # Include
            elif slug == "nba-en-vivo" and e['sport'].lower() == "nba":
                pass # Include
            elif slug == "tarjeta-roja-tv":
                pass # Include all
            else:
                continue
                
            cat_content += f"""
            <a href="/partido/{e['slug']}-en-vivo" class="event-row">
                <div class="event-time">{e['time']}</div>
                <div class="event-sport-icon">📺</div>
                <div class="event-title">{e['title']}</div>
                <div style="color: var(--red); font-weight: bold;">VER &raquo;</div>
            </a>"""
        cat_content += '</div>'
        
        cat_html = get_template(cat_title, cat_desc, cat_url, cat_content)
        with open(os.path.join(OUTPUT_DIR, "categoria", f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(cat_html)

    # 4. Generate Legal & Contact Pages
    print("Generating Legal & Contact Pages...")
    legal_content = """
    <div class="seo-section">
        <h2>Aviso Legal</h2>
        <p>Tarjeta Roja En Vivo es un sitio web que recopila enlaces de transmisiones deportivas disponibles libremente en internet. No alojamos ningún contenido audiovisual en nuestros servidores.</p>
        <p>Todo el contenido mostrado es responsabilidad de sus respectivos autores y plataformas de origen. Si usted es titular de algún derecho y desea solicitar la retirada de un enlace, por favor contacte con la plataforma de origen.</p>
    </div>"""
    legal_html = get_template("Aviso Legal | Tarjeta Roja En Vivo", "Aviso legal y términos de uso de Tarjeta Roja En Vivo.", DOMAIN + "/aviso-legal", legal_content)
    with open(os.path.join(OUTPUT_DIR, "aviso-legal.html"), "w", encoding="utf-8") as f:
        f.write(legal_html)

    contact_content = """
    <div class="seo-section">
        <h2>Contacto</h2>
        <p>Para cualquier consulta, sugerencia o reporte, puede ponerse en contacto con nosotros a través del siguiente correo electrónico:</p>
        <p><strong>contacto@tarjetarojaenvivo.live</strong></p>
    </div>"""
    contact_html = get_template("Contacto | Tarjeta Roja En Vivo", "Contacta con el equipo de Tarjeta Roja En Vivo.", DOMAIN + "/contacto", contact_content)
    with open(os.path.join(OUTPUT_DIR, "contacto.html"), "w", encoding="utf-8") as f:
        f.write(contact_html)

    print(f"Success! Site generated in '{OUTPUT_DIR}' directory.")

if __name__ == "__main__":
    generate_site()
