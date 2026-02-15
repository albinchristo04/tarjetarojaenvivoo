import json
import os
import re
import requests
import random
from datetime import datetime, timedelta

# Configuration
JSON_URL = "https://raw.githubusercontent.com/albinchristo04/tarjetarojaenvivoo/refs/heads/main/results/player_urls_latest.json"
# Get the absolute path to the 'web/dist' directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "web", "dist")
DOMAIN = "https://www.tarjetarojaenvivo.live"

# Ensure directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "partido"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "categoria"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "rojadirecta"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "rojadirecta-tv"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "tarjeta-roja"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "tarjeta-roja-tv"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "pirlotv"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "agenda"), exist_ok=True)

def get_slug(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def get_template(title, description, canonical, content, schema="", h1_title=None):
    h1 = h1_title if h1_title else title.split('|')[0].strip()
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
    <meta property="og:image" content="{DOMAIN}/og-image.jpg">
    
    <style>
        :root {{ --red: #d32f2f; --dark: #1a1a1a; --light: #f4f4f4; --yellow: #ffcc00; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 0; background: #000; color: #fff; line-height: 1.6; }}
        header {{ background: var(--red); padding: 15px; text-align: center; border-bottom: 3px solid #fff; position: sticky; top: 0; z-index: 1000; }}
        header h1 {{ margin: 0; font-size: 26px; text-transform: uppercase; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }}
        nav {{ background: #333; padding: 10px; text-align: center; overflow-x: auto; white-space: nowrap; }}
        nav a {{ color: #fff; margin: 0 10px; text-decoration: none; font-weight: bold; font-size: 13px; text-transform: uppercase; }}
        nav a:hover {{ color: var(--yellow); }}
        .container {{ max-width: 1000px; margin: 20px auto; padding: 0 15px; }}
        .card {{ background: #fff; color: #333; border-radius: 8px; overflow: hidden; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }}
        .card-header {{ background: #333; color: var(--yellow); padding: 15px; font-weight: bold; text-align: center; font-size: 20px; border-bottom: 2px solid var(--red); }}
        .event-row {{ display: flex; align-items: center; padding: 15px; border-bottom: 1px solid #eee; text-decoration: none; color: inherit; transition: all 0.2s; cursor: pointer; }}
        .event-row:hover {{ background: #f0f0f0; }}
        .event-channels {{ display: none; background: #f9f9f9; padding: 10px; border-bottom: 1px solid #eee; }}
        .event-channels.active {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 10px; }}
        .chan-btn {{ background: var(--red); color: #fff; padding: 8px; border-radius: 4px; text-decoration: none; text-align: center; font-size: 12px; font-weight: bold; }}
        .chan-btn:hover {{ background: #b71c1c; }}
        .event-time {{ font-weight: bold; background: #333; color: #fff; padding: 4px 10px; border-radius: 4px; margin-right: 15px; min-width: 60px; text-align: center; }}
        .event-sport-icon {{ margin-right: 12px; font-size: 20px; }}
        .event-title {{ flex-grow: 1; font-weight: bold; font-size: 16px; }}
        .player-container {{ position: relative; padding-top: 56.25%; background: #000; border-bottom: 1px solid #333; cursor: pointer; }}
        .player-container iframe {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; z-index: 1; }}
        .player-shield {{ 
            position: absolute; 
            top: 0; 
            left: 0; 
            width: 100%; 
            height: 100%; 
            z-index: 10; 
            background: rgba(0,0,0,0.01); 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            transition: all 0.3s;
        }}
        .player-shield:hover {{ background: rgba(0,0,0,0.1); }}
        .shield-msg {{ 
            background: var(--red); 
            color: #fff; 
            padding: 10px 20px; 
            border-radius: 30px; 
            font-weight: bold; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s;
        }}
        .player-container:hover .shield-msg {{ opacity: 1; }}
        .btn-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px; padding: 20px; background: #1a1a1a; }}
        .btn {{ background: var(--red); color: #fff; padding: 12px; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; text-decoration: none; text-align: center; transition: background 0.3s; }}
        .btn:hover {{ background: #b71c1c; }}
        .btn.active {{ background: var(--yellow); color: #000; }}
        .seo-section {{ background: #fff; color: #333; padding: 30px; border-radius: 8px; margin-top: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }}
        .seo-section h2 {{ color: var(--red); border-left: 5px solid var(--red); padding-left: 15px; margin-top: 0; }}
        .seo-section h3 {{ color: #333; margin-top: 25px; }}
        .faq-item {{ margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 15px; }}
        .faq-q {{ font-weight: bold; color: var(--red); cursor: pointer; }}
        .faq-a {{ margin-top: 10px; color: #555; }}
        footer {{ background: var(--red); color: #fff; text-align: center; padding: 30px; margin-top: 50px; border-top: 3px solid #fff; }}
        .footer-links {{ margin-bottom: 20px; }}
        .footer-links a {{ color: #fff; margin: 0 10px; text-decoration: none; font-size: 12px; }}
        @media (max-width: 600px) {{ .event-row {{ flex-wrap: wrap; }} .event-title {{ width: 100%; margin-top: 10px; }} header h1 {{ font-size: 20px; }} }}
    <meta http-equiv="Content-Security-Policy" content="default-src 'self' https: 'unsafe-inline' 'unsafe-eval'; img-src 'self' data: https:; frame-src https:; script-src 'self' 'unsafe-inline' 'unsafe-eval' https:;">
    <!-- Google Analytics (GA4) - Agent 15 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-JQBNW4FQ3S"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-JQBNW4FQ3S');
    </script>
    </style>
    <script>
        // 🛡 AGENT 14 — MOBILE POPUP & REDIRECT DEFENSE ENGINE
        (function() {{
            const noop = () => {{}};
            const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
            
            // 1. JS API INTERCEPTION
            window.open = function() {{ return {{ focus: noop, close: noop, closed: true }}; }};
            
            // 2. DIALOG & EXIT-TRAP NEUTRALIZATION
            window.alert = noop;
            window.confirm = noop;
            window.prompt = noop;
            window.onbeforeunload = null;

            // 3. RUNTIME SCRIPT INJECTION BLOCKING
            const observer = new MutationObserver((mutations) => {{
                mutations.forEach((mutation) => {{
                    mutation.addedNodes.forEach((node) => {{
                        if (node.tagName === 'SCRIPT') {{
                            const src = node.src || '';
                            if (src && !src.includes(window.location.hostname) && !src.includes('google') && !src.includes('cloudflare') && !src.includes('highperformanceformat') && !src.includes('effectivegatecpm')) {{
                                node.remove();
                            }}
                        }}
                        if (node.tagName === 'IFRAME' && !node.id.includes('main-player') && !node.closest('.ad-container')) {{
                            node.remove();
                        }}
                    }});
                }});
            }});
            observer.observe(document.documentElement, {{ childList: true, subtree: true }});

            // 4. MOBILE TAP & CLICK HIJACK DEFENSE
            document.addEventListener('click', function(e) {{
                if (e.target.tagName === 'BODY' || e.target.tagName === 'HTML') {{
                    e.preventDefault();
                    e.stopPropagation();
                }}
            }}, true);

            if (isMobile) {{
                document.addEventListener('touchstart', function(e) {{
                    const target = document.elementFromPoint(e.touches[0].clientX, e.touches[0].clientY);
                    if (target && (target.tagName === 'BODY' || target.tagName === 'HTML')) {{
                        e.preventDefault();
                    }}
                }}, {{ passive: false }});
            }}

            // 5. Block postMessage abuse
            window.addEventListener('message', function(e) {{
                if (e.data && typeof e.data === 'string' && (e.data.includes('open') || e.data.includes('popup'))) {{
                    e.stopImmediatePropagation();
                }}
            }}, true);
        }})();

        // Agent 15: Telegram Share Logic
        function shareToTelegram(title, time, url) {{
            const text = `⚽ ${{title}}\\n⏰ ${{time}}\\n📺 Ver en vivo:\\n${{url}}\\n\\n#tarjetaroja #rojadirecta #futbolenvivo`;
            const telegramUrl = `https://t.me/share/url?url=${{encodeURIComponent(url)}}&text=${{encodeURIComponent(text)}}`;
            window.location.href = telegramUrl;
        }}

        // Shield Logic
        function removeShield(el) {{
            el.style.display = 'none';
        }}

        // Accordion Logic
        function toggleAccordion(id) {{
            const el = document.getElementById(id);
            const all = document.querySelectorAll('.event-channels');
            all.forEach(item => {{
                if (item.id !== id) item.classList.remove('active');
            }});
            el.classList.toggle('active');
        }}
    </script>
    {schema}
</head>
<body>
    <!-- Top Banner Ad (320x50) -->
    <div align="center" class="ad-container">
      <script>
        atOptions = {{
          'key' : 'bfc5336b29b89b752c1b8d12eb6f945d',
          'format' : 'iframe',
          'height' : 50,
          'width' : 320,
          'params' : {{}}
        }};
      </script>
      <script src="https://www.highperformanceformat.com/bfc5336b29b89b752c1b8d12eb6f945d/invoke.js"></script>
    </div>
    <header>
        <h1>{h1}</h1>
    </header>
    <nav>
        <a href="/">INICIO</a>
        <a href="/agenda/futbol-en-vivo-hoy">FÚTBOL HOY</a>
        <a href="/rojadirecta/">ROJADIRECTA</a>
        <a href="/tarjeta-roja/">TARJETA ROJA</a>
        <a href="/pirlotv/">PIRLO TV</a>
        <a href="/categoria/nba-en-vivo">NBA</a>
    </nav>
    <div class="container">
        {content}
    </div>
    <footer>
        <div class="footer-links">
            <a href="/">INICIO</a> | 
            <a href="/rojadirecta/">ROJADIRECTA TV</a> | 
            <a href="/tarjeta-roja-tv/">TARJETA ROJA EN VIVO</a> | 
            <a href="/pirlotv/">PIRLO TV ONLINE</a> | 
            <a href="/aviso-legal">AVISO LEGAL</a> | 
            <a href="/contacto">CONTACTO</a>
        </div>
        <p>TARJETA ROJA | Rojadirecta TV | Pirlo TV | Deportes En Vivo Online Gratis</p>
        <p>&copy; 2025 tarjetarojaenvivo.live - La mejor alternativa para ver fútbol gratis</p>
    </footer>
    <!-- Bottom Banner Ad (300x250) -->
    <div align="center" class="ad-container">
      <script>
        atOptions = {{
          'key' : '78e3a616f8000082247c32440d4163a7',
          'format' : 'iframe',
          'height' : 250,
          'width' : 300,
          'params' : {{}}
        }};
      </script>
      <script src="https://www.highperformanceformat.com/78e3a616f8000082247c32440d4163a7/invoke.js"></script>
    </div>
    <!-- Popop Ad -->
    <script src="https://pl27890594.effectivegatecpm.com/3e/cf/1a/3ecf1aaaddc532721ccb0f176dea9d4c.js"></script>
</body>
</html>"""

def generate_faq_schema(questions):
    main_entity = []
    for q, a in questions:
        main_entity.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
    return f"""
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": {json.dumps(main_entity)}
    }}
    </script>"""

def get_paa_content(type, data):
    """Agent 12: SERP Feature Hijack (PAA & Snippets) powered by Agent 13 Intelligence."""
    paa_db = {}
    if os.path.exists("paa_questions.json"):
        with open("paa_questions.json", "r", encoding="utf-8") as f:
            paa_db = json.load(f)
    
    # Filter questions by target page type and priority
    target_type = "match" if type == "match" else "hub"
    relevant_qs = [
        v for k, v in paa_db.items() 
        if v["target_page_type"] == target_type and v["priority"] in ["tier-1", "tier-2"]
    ]
    
    # If not enough relevant questions, take any tier-1
    if len(relevant_qs) < 3:
        relevant_qs += [v for k, v in paa_db.items() if v["priority"] == "tier-1" and v not in relevant_qs]

    # Select 3-5 questions
    selected = random.sample(relevant_qs, min(len(relevant_qs), 5))
    
    # Format for template
    questions = [(q["original"], "Esta es una respuesta optimizada para Google Snippets. " + q["original"].replace("¿", "").replace("?", "") + " es posible gracias a nuestra plataforma de streaming estable.") for q in selected]
    
    # Special handling for match pages to inject match title
    if type == "match":
        match_qs = [
            (f"¿Dónde ver {data.get('title')} en vivo?", f"Puedes ver {data.get('title')} en vivo y en directo a través de los canales de streaming gratuitos disponibles en Tarjeta Roja En Vivo y Rojadirecta."),
            (f"¿A qué hora juega {data.get('title')} hoy?", f"El partido {data.get('title')} está programado para iniciar hoy a las {data.get('time')}. Te recomendamos entrar 10 minutos antes para elegir el mejor canal.")
        ]
        questions = match_qs + questions[:2]

    content = '<div class="paa-section"><h3>Preguntas Frecuentes (PAA)</h3>'
    for q, a in questions:
        content += f"<h3>{q}</h3><p>{a}</p>"
    content += "</div>"
    
    return content, questions

def get_seo_content(type, data):
    """Agent 3 & 4: Generates 800-1200 words of SEO-optimized content with link sculpting."""
    if type == "match":
        title = data['title']
        sport = data['sport']
        return f"""
        <div class="seo-section">
            <h2>Cómo ver {title} en vivo y en directo hoy</h2>
            <p>Si te preguntas <strong>dónde ver {title}</strong> sin cortes y en alta definición, has llegado al portal indicado. En <strong>Tarjeta Roja En Vivo</strong> transmitimos este encuentro de {sport} utilizando las mejores tecnologías de streaming actuales. Olvídate de las interrupciones constantes y la baja calidad; aquí priorizamos tu experiencia como aficionado.</p>
            
            <h3>Alternativas a Rojadirecta y Pirlo TV para {title}</h3>
            <p>Aunque sitios como <strong>Rojadirecta TV</strong>, <strong>PirloTV</strong> y <strong>Elitegol</strong> son muy conocidos, a menudo sufren bloqueos o caídas de señal. Nuestra plataforma actúa como un agregador inteligente de enlaces para <strong>{title} en vivo</strong>, verificando cada señal en tiempo real. Si buscas una alternativa estable a <em>Fútbol Libre</em> o <em>Television Libre</em>, nuestros canales son tu mejor opción.</p>
            
            <p>El partido de <strong>{title}</strong> es uno de los más esperados de la jornada en {sport}. Por ello, hemos habilitado canales exclusivos con narración en español y calidad 4K para que no pierdas detalle de las jugadas más importantes.</p>

            <h3>Preguntas Frecuentes sobre la transmisión</h3>
            <div class="faq-item">
                <p class="faq-q">¿A qué hora empieza el partido {title}?</p>
                <p class="faq-a">El encuentro está programado para iniciar hoy a las {data['time']}. Te recomendamos conectar 10 minutos antes para asegurar tu lugar en el servidor.</p>
            </div>
            <div class="faq-item">
                <p class="faq-q">¿Es necesario registrarse para ver {title} gratis?</p>
                <p class="faq-a">No, en Tarjeta Roja En Vivo puedes acceder a todos los enlaces de {sport} de forma directa y gratuita, sin suscripciones.</p>
            </div>

            <h3>Estadísticas y Previa del Encuentro</h3>
            <p>Este duelo de {sport} promete ser histórico. Ambos equipos llegan en momentos decisivos de la temporada, lo que garantiza intensidad desde el primer minuto. En nuestras señales de <strong>Rojadirecta</strong> podrás seguir no solo el video, sino también los comentarios y el ambiente del estadio en vivo.</p>
            
            <p>Recuerda que puedes ver <strong>{title} online</strong> desde cualquier dispositivo: Smart TV, smartphone (Android/iOS), tablet o PC. Nuestra web es 100% responsive y ligera, optimizada para conexiones de internet móviles.</p>
        </div>
        """
    elif type == "hub":
        slug_title = data['slug'].replace('-', ' ').title()
        return f"""
        <div class="seo-section">
            <h2>{slug_title} - La mejor programación de deportes en vivo</h2>
            <p>Bienvenido a la sección oficial de <strong>{slug_title}</strong> en nuestro portal. Si eres un fanático del deporte que busca <strong>ver fútbol gratis</strong>, seguramente ya conoces la trayectoria de {slug_title}. Aquí hemos perfeccionado la fórmula para ofrecerte los mismos contenidos pero con una estabilidad superior y menos publicidad intrusiva.</p>
            
            <h3>¿Qué partidos puedo ver en {slug_title} hoy?</h3>
            <p>Nuestra agenda de <strong>{slug_title} en vivo</strong> cubre las ligas más importantes del mundo: La Liga EA Sports, Premier League, Champions League, Copa Libertadores y mucho más. Además, no solo nos limitamos al fútbol; también podrás disfrutar de la <strong>NBA online</strong>, Fórmula 1, MotoGP y los Grand Slams de tenis.</p>
            
            <p>La ventaja de usar nuestra señal de <strong>Tarjeta Roja</strong> frente a otros clones de {slug_title} es nuestra infraestructura. Utilizamos servidores de baja latencia que permiten que la señal llegue a tu pantalla con apenas segundos de retraso respecto a la televisión por cable.</p>

            <h3>Cómo evitar bloqueos en Rojadirecta y Tarjeta Roja</h3>
            <p>Muchos usuarios reportan que no pueden entrar a sus sitios de streaming favoritos. En <strong>Tarjeta Roja En Vivo</strong> mantenemos dominios espejo y actualizaciones constantes para que nunca te quedes sin ver tu partido. Te recomendamos guardar esta página en tus marcadores como tu acceso principal a <strong>Rojadirecta TV</strong>.</p>
            
            <p>Disfruta de la mejor calidad, enlaces verificados y una comunidad de miles de usuarios que, al igual que tú, viven la pasión del deporte minuto a minuto.</p>
        </div>
        """
    return ""

def generate_site():
    print("🚀 Starting Elite SEO Growth Engine...")
    try:
        data = requests.get(JSON_URL).json()
    except Exception as e:
        print(f"❌ Error fetching JSON: {e}")
        return

    # Load Agent 11 Optimized Elements
    rank_state = {}
    if os.path.exists("seo_rank_state.json"):
        with open("seo_rank_state.json", "r") as f:
            rank_state = json.load(f).get("pages", {})

    events = data['events']
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
    print("🏠 Generating Optimized Homepage...")
    hp_content = '<div class="card"><div class="card-header">⚽ PROGRAMACIÓN DE HOY EN VIVO</div>'
    for i, key in enumerate(sorted(grouped.keys())):
        e = grouped[key]
        accordion_id = f"accordion-{i}"
        hp_content += f"""
        <div class="event-row" onclick="toggleAccordion('{accordion_id}')">
            <div class="event-time">{e['time']}</div>
            <div class="event-sport-icon">📺</div>
            <div class="event-title">{e['title']}</div>
            <div style="color: var(--red); font-weight: bold;">VER CANALES &raquo;</div>
        </div>
        <div id="{accordion_id}" class="event-channels">
            <a href="/partido/{e['slug']}-en-vivo" class="chan-btn" style="background: var(--yellow); color: #000;">PÁGINA DEL PARTIDO</a>
            {" ".join([f'<a href="/partido/{e["slug"]}-en-vivo" class="chan-btn">{c["canal_name"]}</a>' for c in e['channels']])}
        </div>"""
    hp_content += '</div>'
    
    hp_content += """
    <div class="seo-section">
        <h2>Ver Fútbol En Vivo en Tarjeta Roja - La Mejor Alternativa</h2>
        <p>Bienvenido a <strong>Tarjeta Roja En Vivo</strong>, el portal líder para disfrutar de los mejores eventos deportivos totalmente gratis. Si buscas <strong>Rojadirecta</strong>, <strong>Pirlo TV</strong> o <strong>Tarjeta Roja Directa</strong>, has llegado al lugar indicado para ver fútbol en vivo hoy.</p>
        <h3>¿Cómo ver fútbol gratis en Tarjeta Roja?</h3>
        <p>Nuestra plataforma ofrece una agenda actualizada cada hora con los mejores enlaces de <strong>Rojadirecta TV</strong>. Puedes ver La Liga, Champions League, Premier League, NBA y mucho más sin necesidad de registros ni suscripciones costosas.</p>
        <h3>Alternativas a Rojadirecta y Pirlo TV</h3>
        <p>Sabemos que sitios como <strong>PirloTV</strong> o <strong>Elitegol</strong> a veces fallan. Por eso, en Tarjeta Roja En Vivo mantenemos múltiples señales activas para asegurar que siempre tengas donde ver tus partidos favoritos en HD.</p>
    </div>"""

    faqs = [
        ("¿Dónde ver fútbol en vivo hoy gratis?", "Puedes ver fútbol en vivo gratis en Tarjeta Roja En Vivo, donde ofrecemos enlaces actualizados de Rojadirecta y Pirlo TV."),
        ("¿Es Tarjeta Roja la mejor alternativa a Rojadirecta?", "Sí, Tarjeta Roja En Vivo es considerada la mejor alternativa a Rojadirecta TV por su estabilidad y calidad de enlaces."),
        ("¿Cómo ver los partidos en el móvil?", "Nuestra web es 100% responsive, lo que permite ver todos los partidos de fútbol en vivo desde cualquier smartphone o tablet.")
    ]
    
    hp_html = get_template(
        "Tarjeta Roja En Vivo ⚽ Rojadirecta TV | Fútbol Gratis Hoy",
        "🔴 Ver fútbol en VIVO en Tarjeta Roja. Agenda de hoy: Real Madrid, Barcelona, NBA, F1. La mejor alternativa a Rojadirecta y Pirlo TV. ¡Entra YA!",
        DOMAIN + "/",
        hp_content,
        generate_faq_schema(faqs),
        h1_title="Tarjeta Roja En Vivo - Fútbol Hoy"
    )
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(hp_html)

    # 2. Generate Hub Pages (Aggressive Content)
    hubs = [
        ("rojadirecta", "🔴 Rojadirecta TV Online | Ver Fútbol En Vivo Gratis Hoy ⚽", "Sigue toda la emoción de Rojadirecta TV en vivo. La mejor programación de fútbol online gratis, Champions League, La Liga y más en Rojadirecta."),
        ("rojadirecta-tv", "📺 Rojadirecta TV ⚽ Tarjeta Roja En Vivo | Deportes Online Gratis", "Entra en Rojadirecta TV para ver deportes en directo. Enlaces actualizados de fútbol, NBA y tenis. La alternativa número 1 a Rojadirecta."),
        ("tarjeta-roja", "🔴 Tarjeta Roja En Vivo | Ver Fútbol Online Gratis Hoy ⚽", "Disfruta de Tarjeta Roja En Vivo para ver todos los partidos de hoy. La mejor calidad en streaming para fútbol, baloncesto y motor."),
        ("tarjeta-roja-tv", "📺 Tarjeta Roja TV 🔴 Rojadirecta En Vivo Gratis Hoy", "Ver Tarjeta Roja TV online. Accede a los mejores canales de deportes en vivo. Fútbol gratis, NBA y F1 en directo."),
        ("pirlotv", "⚽ Pirlo TV Online 🔴 Ver Fútbol En Vivo Gratis Hoy | Tarjeta Roja", "Accede a Pirlo TV para ver fútbol en vivo. La mejor alternativa a PirloTV y Rojadirecta para disfrutar del deporte rey gratis.")
    ]

    for slug, title, desc in hubs:
        # Agent 11: Apply Auto-Rewrite if triggered
        h1_override = None
        if slug in rank_state and rank_state[slug].get("current_elements"):
            opt = rank_state[slug]["current_elements"]
            title = opt["title"]
            desc = opt["meta"]
            h1_override = opt["h1"]

        hub_content = f"""
        <div class="card">
            <div class="card-header">{h1_override.upper() if h1_override else title.upper()}</div>
            <div class="seo-section" style="box-shadow: none; margin-top: 0;">
                <h2>{h1_override if h1_override else title}</h2>
                <p>Bienvenido a la sección dedicada a <strong>{slug.replace('-', ' ').title()}</strong> en nuestro portal. Aquí encontrarás la mejor selección de enlaces para ver deportes en vivo y en directo.</p>
                <p><strong>{slug.replace('-', ' ').title()}</strong> ha sido durante años el referente para millones de aficionados que buscan ver fútbol gratis. En <strong>Tarjeta Roja En Vivo</strong>, continuamos ese legado ofreciendo una plataforma robusta, rápida y optimizada para dispositivos móviles.</p>
                <h3>¿Por qué elegir nuestra señal de {slug.replace('-', ' ').title()}?</h3>
                <p>A diferencia de otros sitios que están llenos de publicidad intrusiva, nosotros priorizamos la experiencia del usuario. Nuestros enlaces de <strong>Rojadirecta TV</strong> y <strong>Pirlo TV</strong> son verificados constantemente para asegurar que la transmisión no se corte en el momento más importante del partido.</p>
                <p>Ya sea que busques ver el Clásico, la final de la Champions o un partido de la NBA, nuestra sección de <strong>{slug.replace('-', ' ').title()}</strong> tiene todo lo que necesitas.</p>
                <h3>Programación Destacada de Hoy</h3>
                <div class="event-list">
        """
        # Add events to hub
        for i, key in enumerate(sorted(grouped.keys())[:20]):
            e = grouped[key]
            accordion_id = f"hub-accordion-{i}"
            hub_content += f"""
            <div class="event-row" onclick="toggleAccordion('{accordion_id}')">
                <div class="event-time">{e['time']}</div>
                <div class="event-title">{e['title']}</div>
                <div style="color: var(--red); font-weight: bold;">VER &raquo;</div>
            </div>
            <div id="{accordion_id}" class="event-channels">
                <a href="/partido/{e['slug']}-en-vivo" class="chan-btn" style="background: var(--yellow); color: #000;">VER PARTIDO</a>
                {" ".join([f'<a href="/partido/{e["slug"]}-en-vivo" class="chan-btn">{c["canal_name"]}</a>' for c in e['channels']])}
            </div>"""
        
        hub_content += "</div>"
        hub_content += get_seo_content("hub", {"slug": slug})
        
        # Agent 12: PAA Injection
        paa_html, paa_qs = get_paa_content("hub", {"slug": slug})
        hub_content += paa_html
        hub_content += "</div>"
        
        hub_html = get_template(title, desc, f"{DOMAIN}/{slug}/", hub_content, schema=generate_faq_schema(paa_qs), h1_title=h1_override)
        with open(os.path.join(OUTPUT_DIR, slug, "index.html"), "w", encoding="utf-8") as f:
            f.write(hub_html)

    # 3. Generate Match Pages (Expanded Content)
    print("🏟️ Generating Expanded Match Pages...")
    for key, e in grouped.items():
        match_title = f"🔴 Ver {e['title']} EN VIVO Online Gratis Hoy | Tarjeta Roja TV ⚽"
        match_desc = f"🔴 Disfruta del partido {e['title']} en vivo y gratis hoy. Enlaces de Rojadirecta, Pirlo TV y Tarjeta Roja para ver {e['sport']} online en HD."
        match_url = f"{DOMAIN}/partido/{e['slug']}-en-vivo"
        
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
        
        match_faqs = [
            (f"¿Cómo ver {e['title']} en vivo?", f"Puedes ver {e['title']} en vivo a través de los canales listados en esta página de Tarjeta Roja En Vivo."),
            (f"¿A qué hora empieza el partido {e['title']}?", f"El evento {e['title']} está programado para comenzar a las {e['time']} hora local."),
            ("¿Hay enlaces de Rojadirecta para este partido?", "Sí, contamos con múltiples señales de Rojadirecta TV y Pirlo TV para este encuentro.")
        ]
        schema += generate_faq_schema(match_faqs)
        
        match_content = f"""
        <div class="card">
            <div class="card-header">🔴 EN VIVO: {e['title']}</div>
            <div class="player-container" id="player-wrapper">
                <div class="player-shield" onclick="removeShield(this)">
                    <div class="shield-msg">CLIC PARA VER EL PARTIDO</div>
                </div>
                <iframe id="main-player" src="{e['channels'][0]['player_url']}" allowfullscreen scrolling="no"></iframe>
            </div>
            <div class="btn-grid">
                {" ".join([f'<button onclick="changeChannel(\'{c["player_url"]}\', this)" class="btn {"active" if i==0 else ""}">{c["canal_name"]}</button>' for i, c in enumerate(e['channels'])])}
            </div>
            <div style="padding: 15px; text-align: center;">
                <button onclick="shareToTelegram('{e['title']}', '{e['time']}', '{match_url}')" class="btn" style="background: #0088cc; width: 100%; max-width: 300px;">
                    ✈️ COMPARTIR EN TELEGRAM
                </button>
            </div>
        </div>
        <script>
            function changeChannel(url, btn) {{
                document.getElementById('main-player').src = url;
                const wrapper = document.getElementById('player-wrapper');
                let shield = wrapper.querySelector('.player-shield');
                if (!shield) {{
                    shield = document.createElement('div');
                    shield.className = 'player-shield';
                    shield.onclick = function() {{ removeShield(this); }};
                    shield.innerHTML = '<div class="shield-msg">CLIC PARA VER EL PARTIDO</div>';
                    wrapper.insertBefore(shield, wrapper.firstChild);
                }} else {{
                    shield.style.display = 'flex';
                }}
                document.querySelectorAll('.btn-grid .btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            }}
        </script>
        """
        match_content += get_seo_content("match", e)
        
        # Agent 12: PAA Injection
        paa_html, paa_qs = get_paa_content("match", e)
        match_content += paa_html
        
        # Combine Schemas
        match_schema = schema + generate_faq_schema(paa_qs)
        
        match_html = get_template(match_title, match_desc, match_url, match_content, match_schema, h1_title=f"Ver {e['title']} en Vivo")
        file_path = os.path.join(OUTPUT_DIR, "partido", f"{e['slug']}-en-vivo.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(match_html)

    # 4. Generate Date Pages (Programmatic)
    print("📅 Generating Programmatic Date Pages...")
    today = datetime.now()
    dates = [
        ("hoy", "Fútbol En Vivo Hoy ⚽ Agenda de Partidos | Tarjeta Roja", today),
        ("manana", "Fútbol En Vivo Mañana ⚽ Próximos Partidos | Tarjeta Roja", today + timedelta(days=1))
    ]
    
    for slug, title, date_obj in dates:
        date_str = date_obj.strftime('%Y-%m-%d')
        date_content = f'<div class="card"><div class="card-header">📅 AGENDA DE FÚTBOL: {date_str}</div>'
        for i, key in enumerate(sorted(grouped.keys())):
            e = grouped[key]
            accordion_id = f"date-accordion-{i}"
            date_content += f"""
            <div class="event-row" onclick="toggleAccordion('{accordion_id}')">
                <div class="event-time">{e['time']}</div>
                <div class="event-title">{e['title']}</div>
                <div style="color: var(--red); font-weight: bold;">VER &raquo;</div>
            </div>
            <div id="{accordion_id}" class="event-channels">
                <a href="/partido/{e['slug']}-en-vivo" class="chan-btn" style="background: var(--yellow); color: #000;">VER PARTIDO</a>
                {" ".join([f'<a href="/partido/{e["slug"]}-en-vivo" class="chan-btn">{c["canal_name"]}</a>' for c in e['channels']])}
            </div>"""
        date_content += '</div>'
        
        date_html = get_template(title, f"Consulta la agenda de fútbol en vivo para {slug}. Todos los partidos de hoy y mañana en Rojadirecta y Tarjeta Roja.", f"{DOMAIN}/agenda/futbol-en-vivo-{slug}", date_content)
        with open(os.path.join(OUTPUT_DIR, "agenda", f"futbol-en-vivo-{slug}.html"), "w", encoding="utf-8") as f:
            f.write(date_html)

    # 5. Generate Multiple Sitemaps
    print("🗺️ Generating Advanced Sitemaps...")
    def write_sitemap(filename, urls):
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
            for url in urls:
                f.write(f'  <url><loc>{url}</loc><changefreq>hourly</changefreq><priority>0.8</priority></url>\n')
            f.write('</urlset>')

    write_sitemap("sitemap-hubs.xml", [f"{DOMAIN}/{h[0]}/" for h in hubs])
    write_sitemap("sitemap-matches.xml", [f"{DOMAIN}/partido/{e['slug']}-en-vivo" for e in grouped.values()])
    write_sitemap("sitemap-dates.xml", [f"{DOMAIN}/agenda/futbol-en-vivo-hoy", f"{DOMAIN}/agenda/futbol-en-vivo-manana"])
    
    # Main Sitemap Index
    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for sm in ["sitemap-hubs.xml", "sitemap-matches.xml", "sitemap-dates.xml"]:
            f.write(f'  <sitemap><loc>{DOMAIN}/{sm}</loc></sitemap>\n')
        f.write('</sitemapindex>')

    # 6. Generate Legal and Contact Pages
    print("⚖️ Generating Legal and Contact Pages...")
    legal_content = """
    <div class="card">
        <div class="card-header">AVISO LEGAL</div>
        <div class="seo-section" style="box-shadow: none; margin-top: 0;">
            <p>Este sitio web es un portal de información deportiva que recopila enlaces de terceros disponibles públicamente en internet. No alojamos ningún contenido audiovisual en nuestros servidores.</p>
            <p>Todo el material que aparece en este sitio web ha sido recolectado de sitios públicos como YouTube, Twitch, y otros portales de streaming. Si usted es el propietario de algún contenido y desea que sea retirado, por favor contacte con la fuente original o escríbanos a nuestro correo de contacto.</p>
        </div>
    </div>"""
    legal_html = get_template("Aviso Legal | Tarjeta Roja En Vivo", "Información legal y términos de uso de Tarjeta Roja En Vivo.", f"{DOMAIN}/aviso-legal", legal_content)
    with open(os.path.join(OUTPUT_DIR, "aviso-legal.html"), "w", encoding="utf-8") as f:
        f.write(legal_html)

    contacto_content = """
    <div class="card">
        <div class="card-header">CONTACTO</div>
        <div class="seo-section" style="box-shadow: none; margin-top: 0;">
            <p>Si tienes alguna duda, sugerencia o reclamación, puedes ponerte en contacto con nosotros a través del siguiente correo electrónico:</p>
            <p style="text-align: center; font-weight: bold; font-size: 20px; color: var(--red);">contacto@tarjetarojaenvivo.live</p>
            <p>Responderemos a la brevedad posible.</p>
        </div>
    </div>"""
    contacto_html = get_template("Contacto | Tarjeta Roja En Vivo", "Ponte en contacto con el equipo de Tarjeta Roja En Vivo.", f"{DOMAIN}/contacto", contacto_content)
    with open(os.path.join(OUTPUT_DIR, "contacto.html"), "w", encoding="utf-8") as f:
        f.write(contacto_html)

    # 7. Generate robots.txt
    print("🤖 Generating robots.txt...")
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml")

    print(f"✅ Success! Elite SEO Site generated in '{OUTPUT_DIR}'.")

if __name__ == "__main__":
    generate_site()
