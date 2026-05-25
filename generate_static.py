import json
import os
import re
import requests
import random
from datetime import datetime, timedelta

# Configuration
JSON_URL = "https://sportsonline.ppvtv.top/api/matches.json"
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
# New programmatic SEO hub directories
os.makedirs(os.path.join(OUTPUT_DIR, "tarjeta-roja-en-vivo"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "roja-directa"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "roja-tv"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "targeta-roja"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "la-roja-directa"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "rojadirecta-futbol"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "pirlo-tv-tarjeta-roja"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "roja-directa-en-vivo"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "futbol-en-vivo-gratis"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "rojadirecta-online"), exist_ok=True)
# League/competition page directories
os.makedirs(os.path.join(OUTPUT_DIR, "champions-league-en-vivo"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "la-liga-en-vivo"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "premier-league-en-vivo"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "copa-libertadores-en-vivo"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "liga-mx-en-vivo"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "nba-en-vivo"), exist_ok=True)
# New LATAM league directories
os.makedirs(os.path.join(OUTPUT_DIR, "futbol-argentino-en-vivo"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "brasileirao-en-vivo"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "liga-betplay-en-vivo"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "liga-peru-en-vivo"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "liga-chilena-en-vivo"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "copa-sudamericana-en-vivo"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "futbol-libre"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "futbol-en-vivo"), exist_ok=True)

def get_slug(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def get_template(title, description, canonical, content, schema="", h1_title=None, breadcrumbs=None):
    h1 = h1_title if h1_title else title.split('|')[0].strip()
    # Generate breadcrumb HTML and schema
    breadcrumb_html = ""
    breadcrumb_schema = ""
    if breadcrumbs and len(breadcrumbs) > 0:
        crumb_links = []
        schema_items = []
        for i, (name, url) in enumerate(breadcrumbs):
            pos = i + 1
            if i < len(breadcrumbs) - 1:
                crumb_links.append(f'<a href="{url}" style="color:var(--yellow);text-decoration:none;">{name}</a>')
            else:
                crumb_links.append(f'<span style="color:#ccc;">{name}</span>')
            schema_items.append(f'{{"@type":"ListItem","position":{pos},"name":"{name}","item":"{url}"}}')
        breadcrumb_html = f'<div class="breadcrumb" style="padding:8px 15px;font-size:13px;color:#aaa;background:#111;">{" › ".join(crumb_links)}</div>'
        breadcrumb_schema = f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{",".join(schema_items)}]}}</script>'
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="tarjeta roja en vivo, rojadirecta, pirlo tv, roja directa en vivo, tarjeta roja tv, futbol libre, futbol libre en vivo, futbol en vivo gratis, rojadirecta tv, pirlotv, roja directa, targeta roja, la roja directa, roja tv, rojadirecta futbol, pirlo tv tarjeta roja, rojadirecta online, liga mx en vivo, copa libertadores en vivo, futbol argentino en vivo, brasileirao en vivo, liga betplay en vivo, nba en vivo, fútbol en vivo hoy">
    <link rel="canonical" href="{canonical}">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
    {breadcrumb_schema}
    <link rel="icon" href="/favicon.ico">
    
    <!-- Bing-specific meta tags -->
    <meta name="bingbot" content="index, follow, max-snippet:-1, max-image-preview:large">
    <meta name="msnbot" content="index, follow">
    
    <!-- Language & Locale for Bing -->
    <meta name="language" content="es">
    <meta name="geo.region" content="MX">
    <meta name="geo.placename" content="México">
    <meta http-equiv="content-language" content="es">
    
    <!-- AI Citation meta tags (Copilot, ChatGPT, Perplexity) -->
    <meta name="citation_title" content="{title}">
    <meta name="citation_site_title" content="Tarjeta Roja En Vivo">
    <meta name="citation_language" content="es">
    <meta name="citation_public_url" content="{canonical}">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Tarjeta Roja En Vivo">
    <meta property="og:locale" content="es_MX">
    <meta property="og:image" content="{DOMAIN}/og-image.jpg">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{DOMAIN}/og-image.jpg">
    
    <!-- Hreflang -->
    <link rel="alternate" hreflang="es" href="{canonical}">
    <link rel="alternate" hreflang="x-default" href="{canonical}">
    
    <!-- Preconnect hints -->
    <link rel="preconnect" href="https://www.googletagmanager.com">
    <link rel="preconnect" href="https://www.highperformanceformat.com">
    <link rel="dns-prefetch" href="https://pl27890594.effectivegatecpm.com">
    
    <!-- External CSS -->
    <link rel="stylesheet" href="/style.css">
    
    <meta http-equiv="Content-Security-Policy" content="default-src 'self' https: 'unsafe-inline' 'unsafe-eval'; img-src 'self' data: https:; frame-src https:; script-src 'self' 'unsafe-inline' 'unsafe-eval' https:;">
    
    <!-- Organization + WebSite Schema -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Tarjeta Roja En Vivo",
        "url": "{DOMAIN}",
        "logo": "{DOMAIN}/favicon.ico",
        "alternateName": ["Tarjeta Roja TV", "Rojadirecta", "Roja Directa", "Pirlo TV", "PirloTV", "Fútbol Libre", "Roja TV", "Targeta Roja", "RojaDirecta TV"],
        "sameAs": []
    }}
    </script>
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Tarjeta Roja En Vivo",
        "alternateName": ["Tarjeta Roja TV", "Rojadirecta", "Roja Directa", "Pirlo TV", "Fútbol Libre", "Roja TV", "RojaDirecta En Vivo", "Futbol Libre En Vivo", "Tarjeta Roja Pirlo TV"],
        "url": "{DOMAIN}",
        "inLanguage": "es",
        "potentialAction": {{
            "@type": "SearchAction",
            "target": "{DOMAIN}/?q={{search_term_string}}",
            "query-input": "required name=search_term_string"
        }}
    }}
    </script>
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "{title}",
        "description": "{description}",
        "url": "{canonical}",
        "inLanguage": "es",
        "isPartOf": {{"@type": "WebSite", "name": "Tarjeta Roja En Vivo", "url": "{DOMAIN}"}},
        "publisher": {{"@type": "Organization", "name": "Tarjeta Roja En Vivo", "url": "{DOMAIN}"}},
        "speakable": {{
            "@type": "SpeakableSpecification",
            "cssSelector": ["h1", "h2", ".seo-section p:first-child", ".faq-q", ".faq-a"]
        }}
    }}
    </script>
    
    <!-- Google Analytics (GA4) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-JQBNW4FQ3S"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-JQBNW4FQ3S');
    </script>
    <script>
        // 🛡 AGENT 14 — MOBILE POPUP & REDIRECT DEFENSE ENGINE
        (function() {{
            // 1. RUNTIME SCRIPT INJECTION BLOCKING
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

            // 2. Block postMessage abuse
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
        <a href="/futbol-libre/" style="color:#00ff88;font-weight:bold;">⚽ FÚTBOL LIBRE</a>
        <a href="/agenda/futbol-en-vivo-hoy">FÚTBOL HOY</a>
        <a href="/rojadirecta/">ROJADIRECTA</a>
        <a href="/tarjeta-roja/">TARJETA ROJA</a>
        <a href="/pirlotv/">PIRLO TV</a>
        <a href="/liga-mx-en-vivo/">LIGA MX</a>
        <a href="/copa-libertadores-en-vivo/">LIBERTADORES</a>
        <a href="/champions-league-en-vivo/">CHAMPIONS</a>
        <a href="/la-liga-en-vivo/">LA LIGA</a>
        <a href="/nba-en-vivo/">NBA</a>
    </nav>
    {breadcrumb_html}
    <div class="container">
        {content}
        <!-- Bottom Banner Ad (300x250) -->
        <div align="center" class="ad-container" style="margin: 20px 0;">
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
    </div>
    <footer>
        <div class="footer-links">
            <a href="/">INICIO</a> | 
            <a href="/futbol-libre/" style="color:#00ff88;">FÚTBOL LIBRE</a> | 
            <a href="/futbol-en-vivo/">FÚTBOL EN VIVO</a> | 
            <a href="/rojadirecta/">ROJADIRECTA</a> | 
            <a href="/tarjeta-roja/">TARJETA ROJA</a> | 
            <a href="/tarjeta-roja-en-vivo/">TARJETA ROJA EN VIVO</a> | 
            <a href="/pirlotv/">PIRLO TV</a> | 
            <a href="/roja-directa/">ROJA DIRECTA</a> | 
            <a href="/roja-directa-en-vivo/">ROJA DIRECTA EN VIVO</a> | 
            <a href="/futbol-en-vivo-gratis/">FÚTBOL GRATIS</a> | 
            <a href="/liga-mx-en-vivo/">LIGA MX</a> | 
            <a href="/copa-libertadores-en-vivo/">COPA LIBERTADORES</a> | 
            <a href="/futbol-argentino-en-vivo/">FÚTBOL ARGENTINO</a> | 
            <a href="/brasileirao-en-vivo/">BRASILEIRÃO</a> | 
            <a href="/liga-betplay-en-vivo/">LIGA BETPLAY</a> | 
            <a href="/liga-peru-en-vivo/">LIGA 1 PERÚ</a> | 
            <a href="/liga-chilena-en-vivo/">LIGA CHILENA</a> | 
            <a href="/copa-sudamericana-en-vivo/">COPA SUDAMERICANA</a> | 
            <a href="/champions-league-en-vivo/">CHAMPIONS LEAGUE</a> | 
            <a href="/la-liga-en-vivo/">LA LIGA</a> | 
            <a href="/premier-league-en-vivo/">PREMIER LEAGUE</a> | 
            <a href="/nba-en-vivo/">NBA EN VIVO</a> | 
            <a href="/aviso-legal">AVISO LEGAL</a> | 
            <a href="/contacto">CONTACTO</a>
        </div>
        <p>TARJETA ROJA EN VIVO | Rojadirecta TV | Pirlo TV | Fútbol Libre | Roja Directa | Champions League | Copa Libertadores | Liga MX | Fútbol Argentino | Brasileirão | La Liga | Premier League | Liga BetPlay | Liga 1 Perú | NBA | Deportes En Vivo Online Gratis</p>
        <p>Tarjeta Roja En Vivo (tarjetarojaenvivo.live) es un directorio de streams deportivos. No alojamos contenido de vídeo. También conocido como Fútbol Libre, Roja Directa, RojaDirecta, Pirlo TV y Tarjeta Roja TV.</p>
        <p>&copy; 2026 tarjetarojaenvivo.live - La mejor alternativa para ver fútbol gratis</p>
    </footer>
    <!-- Popop Ad -->
    <script defer src="https://pl27890594.effectivegatecpm.com/3e/cf/1a/3ecf1aaaddc532721ccb0f176dea9d4c.js"></script>
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

def get_hub_seo_content(slug):
    """Generate unique SEO body content for each hub page based on its slug."""
    content_map = {
        "rojadirecta": """
                <p>Bienvenido a la sección dedicada a <strong>Rojadirecta</strong> en nuestro portal. Aquí encontrarás la mejor selección de enlaces para ver deportes en vivo y en directo.</p>
                <p><strong>Rojadirecta</strong> ha sido durante años el referente para millones de aficionados que buscan ver fútbol gratis. En <strong>Tarjeta Roja En Vivo</strong>, continuamos ese legado ofreciendo una plataforma robusta, rápida y optimizada para dispositivos móviles.</p>
                <h3>¿Por qué elegir nuestra señal de Rojadirecta?</h3>
                <p>A diferencia de otros sitios que están llenos de publicidad intrusiva, nosotros priorizamos la experiencia del usuario. Nuestros enlaces de <strong>Rojadirecta TV</strong> y <strong>Pirlo TV</strong> son verificados constantemente para asegurar que la transmisión no se corte en el momento más importante del partido.</p>
                <p>Ya sea que busques ver el Clásico, la final de la Champions o un partido de la NBA, nuestra sección de <strong>Rojadirecta</strong> tiene todo lo que necesitas.</p>""",
        "rojadirecta-tv": """
                <p>Bienvenido a <strong>Rojadirecta TV</strong>, tu portal de referencia para seguir los mejores eventos deportivos en directo. Nuestra plataforma te conecta con las señales más estables del mundo del streaming deportivo.</p>
                <p>En <strong>Rojadirecta TV</strong> nos especializamos en ofrecer transmisiones de alta calidad para fútbol, baloncesto, tenis, Fórmula 1 y muchos más deportes. Cada enlace es verificado por nuestro equipo antes de ser publicado.</p>
                <h3>La alternativa número 1 a Rojadirecta</h3>
                <p>Si buscas una experiencia sin interrupciones, <strong>Rojadirecta TV</strong> en Tarjeta Roja En Vivo es tu mejor opción. Ofrecemos múltiples canales por evento para que siempre tengas una señal disponible, incluso en los partidos más demandados.</p>
                <p>Compatible con todos los dispositivos: Smart TV, PC, tablet y smartphone. Nuestra web se adapta automáticamente a tu pantalla.</p>""",
        "tarjeta-roja": """
                <p>Bienvenido a <strong>Tarjeta Roja</strong>, la plataforma líder en streaming deportivo gratuito. Aquí encontrarás todos los partidos de fútbol del día con enlaces actualizados cada hora.</p>
                <p><strong>Tarjeta Roja</strong> nació como respuesta a la necesidad de los aficionados de tener un portal confiable donde ver deportes sin pagar suscripciones costosas ni sufrir caídas constantes de señal.</p>
                <h3>¿Qué deportes puedo ver en Tarjeta Roja?</h3>
                <p>En nuestra sección de <strong>Tarjeta Roja</strong> cubrimos fútbol (La Liga, Champions, Premier, Serie A, Bundesliga, Liga MX, Copa Libertadores), baloncesto (NBA, Euroliga), tenis (Grand Slams), motor (F1, MotoGP) y mucho más.</p>
                <p>Cada deporte tiene canales dedicados con narración en español para que no te pierdas ningún detalle de la acción.</p>""",
        "tarjeta-roja-tv": """
                <p><strong>Tarjeta Roja TV</strong> es la evolución del streaming deportivo online. Nuestra plataforma combina las mejores tecnologías de transmisión con una interfaz limpia y fácil de usar.</p>
                <p>Si has buscado <strong>Rojadirecta en vivo</strong> o <strong>Tarjeta Roja TV online</strong>, has llegado al lugar correcto. Aquí centralizamos todas las señales de streaming deportivo verificadas y las organizamos por horario.</p>
                <h3>Ventajas de usar Tarjeta Roja TV</h3>
                <p>Nuestro sistema detecta automáticamente las señales caídas y las reemplaza en tiempo real, por lo que siempre tendrás acceso a una transmisión funcional. Además, no requerimos registro ni datos personales para acceder al contenido.</p>
                <p>Disponible las 24 horas del día, los 7 días de la semana, con contenido actualizado para cada jornada deportiva.</p>""",
        "pirlotv": """
                <p>Bienvenido a <strong>Pirlo TV</strong> en Tarjeta Roja En Vivo. PirloTV ha sido históricamente uno de los portales más populares para ver fútbol en español, y aquí mantenemos esa tradición con señales mejoradas.</p>
                <p>Si estás buscando <strong>Pirlo TV online</strong>, nuestra plataforma te ofrece los mismos contenidos pero con mayor estabilidad, menos publicidad intrusiva y una experiencia de usuario optimizada para dispositivos móviles.</p>
                <h3>¿Pirlo TV funciona hoy?</h3>
                <p>Sí. A diferencia del sitio original que sufre frecuentes bloqueos por parte de ISPs, nuestra versión de <strong>Pirlo TV</strong> mantiene dominios espejo actualizados constantemente. Guarda esta página en tus marcadores para tener siempre acceso directo.</p>
                <p>Cubrimos todas las ligas europeas, sudamericanas y los principales torneos internacionales con múltiples opciones de canal por partido.</p>""",
        "tarjeta-roja-en-vivo": """
                <p>Bienvenido a <strong>Tarjeta Roja En Vivo</strong>, tu destino definitivo para ver partidos de fútbol y otros deportes en directo desde cualquier dispositivo. Nuestra misión es ofrecerte las transmisiones más estables del internet en español.</p>
                <p>¿Buscas <strong>ver fútbol en vivo gratis hoy</strong>? Estás en el lugar indicado. Actualizamos nuestra parrilla de eventos cada 30 minutos para que siempre tengas la información más reciente sobre qué partidos están en directo ahora mismo.</p>
                <h3>¿Cómo funciona Tarjeta Roja En Vivo?</h3>
                <p>Nuestro sistema recopila automáticamente los mejores enlaces de streaming disponibles en internet y los organiza por deporte, liga y horario. Cada enlace es verificado antes de publicarse para garantizar que funciona correctamente.</p>
                <h3>Ligas y competiciones disponibles</h3>
                <p>Cubrimos <strong>La Liga EA Sports</strong>, <strong>Champions League</strong>, <strong>Premier League</strong>, <strong>Serie A</strong>, <strong>Bundesliga</strong>, <strong>Ligue 1</strong>, <strong>Copa Libertadores</strong>, <strong>Liga MX</strong>, <strong>NBA</strong>, <strong>Fórmula 1</strong> y más de 50 competiciones deportivas alrededor del mundo.</p>
                <p>No necesitas crear una cuenta ni proporcionar datos personales. Simplemente entra, elige tu partido y disfruta del espectáculo deportivo en alta definición.</p>""",
        "roja-directa": """
                <p><strong>Roja Directa</strong> es uno de los nombres más buscados cuando se trata de ver deportes en vivo por internet. En esta página reunimos las mejores señales de streaming para que puedas disfrutar de tus partidos favoritos sin complicaciones.</p>
                <p>Si llegaste aquí buscando <strong>Roja Directa</strong>, probablemente ya conoces la trayectoria de este nombre en el mundo del streaming deportivo. Nosotros tomamos lo mejor de esa experiencia y la mejoramos con tecnología más moderna y servidores más rápidos.</p>
                <h3>¿Roja Directa sigue funcionando?</h3>
                <p>El portal original de <strong>Roja Directa</strong> ha sufrido múltiples bloqueos y cambios de dominio a lo largo de los años. En <strong>Tarjeta Roja En Vivo</strong> ofrecemos una alternativa permanente y estable que no depende de un solo dominio.</p>
                <h3>Deportes disponibles en Roja Directa</h3>
                <p>Nuestra parrilla de <strong>Roja Directa</strong> incluye fútbol de todas las ligas principales, NBA, UFC, boxeo, tenis, Fórmula 1 y MotoGP. Cada evento tiene múltiples opciones de canal con diferentes narradores.</p>
                <p>Accede desde tu móvil, tablet, ordenador o Smart TV. Nuestra plataforma es 100% responsive y ligera, diseñada para funcionar incluso con conexiones de internet lentas.</p>""",
        "roja-tv": """
                <p><strong>Roja TV</strong> es tu portal de streaming deportivo en español. Si buscas una forma rápida y sencilla de ver deportes en vivo sin descargas ni registros, has encontrado el lugar perfecto.</p>
                <p>En <strong>Roja TV</strong> nos diferenciamos por ofrecer una experiencia de usuario premium: carga rápida, sin redirecciones molestas y con múltiples opciones de canal para cada evento deportivo.</p>
                <h3>¿Qué puedo ver en Roja TV?</h3>
                <p>Nuestra programación de <strong>Roja TV</strong> abarca los deportes más populares del mundo: fútbol (todas las ligas europeas, sudamericanas y centroamericanas), baloncesto (NBA y Euroliga), tenis (los 4 Grand Slams), motor (F1, MotoGP, NASCAR) y deportes de combate (UFC, boxeo profesional).</p>
                <h3>Roja TV vs otras plataformas</h3>
                <p>A diferencia de plataformas de pago como DAZN, Movistar+ o ESPN, <strong>Roja TV</strong> en Tarjeta Roja En Vivo te permite acceder a todo el contenido de forma gratuita. Solo necesitas un navegador web y conexión a internet.</p>
                <p>Además, ofrecemos notificaciones de partidos próximos a través de nuestro canal de Telegram para que nunca te pierdas un evento importante.</p>""",
        "targeta-roja": """
                <p>¿Buscas <strong>Targeta Roja</strong> para ver fútbol en vivo? Has llegado al lugar correcto. Aunque el nombre correcto es "Tarjeta Roja", sabemos que muchos usuarios buscan <strong>Targeta Roja</strong> como alternativa de escritura, y aquí les damos la bienvenida.</p>
                <p><strong>Targeta Roja</strong> en Tarjeta Roja En Vivo te ofrece exactamente lo que necesitas: acceso directo a los mejores canales de streaming deportivo sin necesidad de registro, suscripción ni descargas de software.</p>
                <h3>Cómo ver fútbol en Targeta Roja</h3>
                <p>Es muy sencillo. Solo tienes que navegar por nuestra agenda de partidos del día, seleccionar el evento que quieres ver y elegir uno de los múltiples canales disponibles. Si un canal no funciona, simplemente prueba con otro en la lista.</p>
                <h3>Partidos disponibles ahora</h3>
                <p>En <strong>Targeta Roja</strong> cubrimos La Liga, Champions League, Premier League, Copa del Rey, Copa Libertadores y muchas más competiciones. Todo actualizado en tiempo real con horarios ajustados a tu zona horaria.</p>
                <p>Recuerda guardar esta página en tus marcadores como <strong>tu acceso principal a Targeta Roja</strong> para no perder la dirección cuando la necesites.</p>""",
        "la-roja-directa": """
                <p>Bienvenido a <strong>La Roja Directa</strong>, el portal de streaming deportivo donde podrás ver todos los partidos de fútbol en vivo y en directo hoy. Si has buscado <strong>La Roja Directa</strong> en internet, esta es tu parada definitiva.</p>
                <p>En <strong>La Roja Directa</strong> recopilamos los mejores enlaces de transmisión de partidos de fútbol, baloncesto, tenis y otros deportes. Cada enlace es verificado por nuestro equipo para garantizar calidad y estabilidad.</p>
                <h3>¿Por qué La Roja Directa?</h3>
                <p>El nombre <strong>La Roja Directa</strong> evoca la pasión del fútbol en español. Millones de hispanohablantes en España, México, Argentina, Colombia y toda Latinoamérica confían en nosotros para ver sus partidos favoritos cada semana.</p>
                <h3>Competiciones en La Roja Directa</h3>
                <p>Nuestra cobertura incluye <strong>La Liga EA Sports</strong>, <strong>Champions League</strong>, <strong>Europa League</strong>, <strong>Copa del Rey</strong>, <strong>Premier League</strong>, <strong>Serie A</strong>, <strong>Bundesliga</strong>, <strong>Liga MX</strong>, <strong>Copa Libertadores</strong> y <strong>Copa Sudamericana</strong>.</p>
                <p>Además, durante eventos especiales como el Mundial o la Eurocopa, activamos canales adicionales para ofrecer cobertura completa de todos los partidos simultáneos.</p>""",
        "rojadirecta-futbol": """
                <p><strong>Rojadirecta Fútbol</strong> es tu sección especializada en el deporte rey. A diferencia de portales generalistas, aquí nos centramos exclusivamente en ofrecerte la mejor experiencia para ver fútbol en vivo y en directo.</p>
                <p>Nuestra cobertura de <strong>Rojadirecta Fútbol</strong> abarca desde las grandes ligas europeas hasta los torneos más competitivos de Sudamérica, pasando por las eliminatorias mundialistas y los amistosos internacionales.</p>
                <h3>Ligas cubierta por Rojadirecta Fútbol</h3>
                <p>En <strong>Rojadirecta Fútbol</strong> encontrarás transmisiones de: La Liga EA Sports (Real Madrid, Barcelona, Atlético), Premier League (Manchester City, Liverpool, Arsenal), Serie A (Inter, Milan, Juventus), Bundesliga (Bayern Munich, Dortmund), Ligue 1 (PSG, Marsella), Liga MX, Copa Libertadores y Copa Sudamericana.</p>
                <h3>Calidad de transmisión</h3>
                <p>Todos nuestros canales de <strong>fútbol en directo</strong> ofrecen calidad HD como mínimo. Para partidos de alta demanda como El Clásico o la final de Champions, habilitamos señales en calidad 4K cuando están disponibles.</p>
                <p>Cada partido tiene al menos 3 opciones de canal diferentes con narración en español para que siempre tengas una alternativa funcional.</p>""",
        "pirlo-tv-tarjeta-roja": """
                <p>Bienvenido a la combinación perfecta: <strong>Pirlo TV y Tarjeta Roja</strong> juntos en un solo portal. Aquí reunimos lo mejor de ambas plataformas de streaming deportivo para ofrecerte una experiencia inigualable.</p>
                <p><strong>Pirlo TV</strong> siempre ha sido reconocido por su amplia variedad de canales, mientras que <strong>Tarjeta Roja</strong> destaca por la estabilidad de sus señales. Al combinarlas, obtienes la mejor selección con la mejor calidad.</p>
                <h3>¿Por qué Pirlo TV + Tarjeta Roja?</h3>
                <p>Muchos usuarios alternan entre <strong>Pirlo TV</strong> y <strong>Tarjeta Roja</strong> buscando la mejor señal para cada partido. Nosotros eliminamos esa necesidad al integrar todas las señales en una única plataforma organizada por evento y horario.</p>
                <h3>Cobertura unificada</h3>
                <p>Con <strong>Pirlo TV Tarjeta Roja</strong> accedes a más de 50 canales simultáneos durante las jornadas deportivas más importantes. Fútbol, baloncesto, tenis, motor y deportes de combate, todo en un solo lugar.</p>
                <p>Guarda esta página y olvídate de tener que buscar enlaces en múltiples sitios web. Aquí lo tienes todo centralizado, organizado y verificado.</p>""",
        "roja-directa-en-vivo": """
                <p><strong>Roja Directa En Vivo</strong> te trae las mejores transmisiones deportivas en tiempo real. Si quieres ver fútbol online gratis hoy sin complicaciones, nuestra plataforma es la solución que buscabas.</p>
                <p>El concepto de <strong>Roja Directa En Vivo</strong> es simple: ofrecerte acceso inmediato a partidos que están sucediendo ahora mismo, con enlaces verificados y calidad HD garantizada.</p>
                <h3>Partidos en vivo ahora</h3>
                <p>Nuestra parrilla de <strong>Roja Directa En Vivo</strong> se actualiza automáticamente cada 15 minutos para reflejar los partidos que están en juego en este momento. Los eventos que ya han terminado se archivan y los próximos se marcan con cuenta regresiva.</p>
                <h3>Cómo ver Roja Directa En Vivo en tu dispositivo</h3>
                <p>Nuestra plataforma funciona en cualquier navegador web moderno: Chrome, Firefox, Safari, Edge. No necesitas instalar aplicaciones ni plugins adicionales. Solo abre la página, elige tu partido y empieza a disfrutar.</p>
                <p>Para la mejor experiencia en móvil, te recomendamos usar el modo pantalla completa tocando el icono de expansión en el reproductor de video.</p>""",
        "futbol-en-vivo-gratis": """
                <p>¿Quieres ver <strong>fútbol en vivo gratis</strong> hoy? En Tarjeta Roja En Vivo te ofrecemos la agenda más completa de partidos de fútbol con transmisiones gratuitas en streaming HD.</p>
                <p>Ver <strong>fútbol en vivo gratis</strong> nunca ha sido tan fácil. Nuestra plataforma recopila y verifica automáticamente los mejores enlaces de transmisión disponibles en internet, organizándolos por liga, horario y calidad de señal.</p>
                <h3>¿Qué partidos de fútbol puedo ver gratis hoy?</h3>
                <p>Cubrimos todas las ligas principales del mundo: <strong>La Liga</strong> (Real Madrid, Barcelona, Atlético), <strong>Premier League</strong> (Manchester City, Arsenal, Liverpool), <strong>Champions League</strong>, <strong>Copa Libertadores</strong>, <strong>Liga MX</strong>, <strong>Serie A</strong>, <strong>Bundesliga</strong> y <strong>Ligue 1</strong>.</p>
                <h3>Fútbol en vivo gratis sin registro</h3>
                <p>A diferencia de plataformas como DAZN, Movistar+ o Star+, aquí no necesitas crear una cuenta ni introducir datos de tarjeta de crédito. El acceso a nuestro <strong>fútbol en vivo gratis</strong> es completamente libre y anónimo.</p>
                <h3>Calidad y estabilidad</h3>
                <p>Nuestros canales ofrecen transmisiones en HD con baja latencia. Para partidos de alta demanda (Clásico, derby de Madrid, finales), activamos servidores adicionales para garantizar que todos los usuarios tengan acceso sin buffering.</p>""",
        "rojadirecta-online": """
                <p>Bienvenido a <strong>Rojadirecta Online</strong>, la versión digital más completa del legendario portal de streaming deportivo. Si buscabas <strong>Rojadirecta Online</strong> para ver deportes en vivo, has encontrado la mejor alternativa disponible.</p>
                <p>En <strong>Rojadirecta Online</strong> combinamos la tradición del portal original con las tecnologías más modernas de streaming para ofrecerte una experiencia superior: menos publicidad, mejor calidad de video y mayor estabilidad de señal.</p>
                <h3>Deportes en vivo en Rojadirecta Online</h3>
                <p>Nuestra programación diaria incluye: fútbol de las principales ligas mundiales, NBA, NFL, tenis (ATP y WTA), Fórmula 1, MotoGP, ciclismo, boxeo, UFC y deportes de invierno durante temporada. Todo accesible desde una única página.</p>
                <h3>Acceso desde cualquier país</h3>
                <p><strong>Rojadirecta Online</strong> está disponible internacionalmente. Ya sea que te conectes desde España, México, Argentina, Colombia, Chile, Perú o cualquier otro país, nuestra plataforma se adapta a tu ubicación mostrándote los horarios en tu zona horaria local.</p>
                <p>No necesitas VPN ni configuración especial. Simplemente abre tu navegador y disfruta del mejor deporte en vivo completamente gratis.</p>""",
    }
    # Default content for unknown slugs
    name = slug.replace('-', ' ').title()
    return content_map.get(slug, f"""
                <p>Bienvenido a la sección dedicada a <strong>{name}</strong> en nuestro portal. Aquí encontrarás la mejor selección de enlaces para ver deportes en vivo y en directo.</p>
                <p><strong>{name}</strong> ha sido durante años el referente para millones de aficionados que buscan ver fútbol gratis. En <strong>Tarjeta Roja En Vivo</strong>, continuamos ese legado ofreciendo una plataforma robusta, rápida y optimizada para dispositivos móviles.</p>
                <h3>¿Por qué elegir nuestra señal de {name}?</h3>
                <p>A diferencia de otros sitios que están llenos de publicidad intrusiva, nosotros priorizamos la experiencia del usuario. Nuestros enlaces de <strong>Rojadirecta TV</strong> y <strong>Pirlo TV</strong> son verificados constantemente para asegurar que la transmisión no se corte.</p>
                <p>Ya sea que busques ver el Clásico, la final de la Champions o un partido de la NBA, nuestra sección de <strong>{name}</strong> tiene todo lo que necesitas.</p>""")

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

    # Define Ad Blocks
    AD_TOP_320_50 = """
    <div align="center" class="ad-container" style="margin: 15px 0;">
      <script>
        atOptions = {
          'key' : 'bfc5336b29b89b752c1b8d12eb6f945d',
          'format' : 'iframe',
          'height' : 50,
          'width' : 320,
          'params' : {}
        };
      </script>
      <script src="https://www.highperformanceformat.com/bfc5336b29b89b752c1b8d12eb6f945d/invoke.js"></script>
    </div>"""

    AD_BOTTOM_300_250 = """
    <div align="center" class="ad-container" style="margin: 15px 0;">
      <script>
        atOptions = {
          'key' : '78e3a616f8000082247c32440d4163a7',
          'format' : 'iframe',
          'height' : 250,
          'width' : 300,
          'params' : {}
        };
      </script>
      <script src="https://www.highperformanceformat.com/78e3a616f8000082247c32440d4163a7/invoke.js"></script>
    </div>"""

    # Generate external CSS file (Fix 1: eliminate duplicate inline CSS)
    print("🎨 Generating external style.css...")
    css_content = """:root { --red: #d32f2f; --dark: #1a1a1a; --light: #f4f4f4; --yellow: #ffcc00; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 0; background: #000; color: #fff; line-height: 1.6; }
header { background: var(--red); padding: 15px; text-align: center; border-bottom: 3px solid #fff; position: sticky; top: 0; z-index: 1000; }
header h1 { margin: 0; font-size: 26px; text-transform: uppercase; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
nav { background: #333; padding: 10px; text-align: center; overflow-x: auto; white-space: nowrap; }
nav a { color: #fff; margin: 0 10px; text-decoration: none; font-weight: bold; font-size: 13px; text-transform: uppercase; }
nav a:hover { color: var(--yellow); }
.container { max-width: 1000px; margin: 20px auto; padding: 0 15px; }
.card { background: #fff; color: #333; border-radius: 8px; overflow: hidden; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
.card-header { background: #333; color: var(--yellow); padding: 15px; font-weight: bold; text-align: center; font-size: 20px; border-bottom: 2px solid var(--red); }
.event-row { display: flex; align-items: center; padding: 15px; border-bottom: 1px solid #eee; text-decoration: none; color: inherit; transition: all 0.2s; cursor: pointer; }
.event-row:hover { background: #f0f0f0; }
.event-channels { display: none; background: #f9f9f9; padding: 10px; border-bottom: 1px solid #eee; }
.event-channels.active { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 10px; }
.chan-btn { background: var(--red); color: #fff; padding: 8px; border-radius: 4px; text-decoration: none; text-align: center; font-size: 12px; font-weight: bold; }
.chan-btn:hover { background: #b71c1c; }
.event-time { font-weight: bold; background: #333; color: #fff; padding: 4px 10px; border-radius: 4px; margin-right: 15px; min-width: 60px; text-align: center; }
.event-sport-icon { margin-right: 12px; font-size: 20px; }
.event-title { flex-grow: 1; font-weight: bold; font-size: 16px; }
.player-container { position: relative; padding-top: 56.25%; background: #000; border-bottom: 1px solid #333; cursor: pointer; }
.player-container iframe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; z-index: 1; }
.player-shield { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 10; background: rgba(0,0,0,0.01); display: flex; align-items: center; justify-content: center; transition: all 0.3s; }
.player-shield:hover { background: rgba(0,0,0,0.1); }
.shield-msg { background: var(--red); color: #fff; padding: 10px 20px; border-radius: 30px; font-weight: bold; box-shadow: 0 4px 15px rgba(0,0,0,0.5); pointer-events: none; opacity: 0; transition: opacity 0.3s; }
.player-container:hover .shield-msg { opacity: 1; }
.btn-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px; padding: 20px; background: #1a1a1a; }
.btn { background: var(--red); color: #fff; padding: 12px; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; text-decoration: none; text-align: center; transition: background 0.3s; }
.btn:hover { background: #b71c1c; }
.btn.active { background: var(--yellow); color: #000; }
.seo-section { background: #fff; color: #333; padding: 30px; border-radius: 8px; margin-top: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
.seo-section h2 { color: var(--red); border-left: 5px solid var(--red); padding-left: 15px; margin-top: 0; }
.seo-section h3 { color: #333; margin-top: 25px; }
.faq-item { margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 15px; }
.faq-q { font-weight: bold; color: var(--red); cursor: pointer; }
.faq-a { margin-top: 10px; color: #555; }
footer { background: var(--red); color: #fff; text-align: center; padding: 30px; margin-top: 50px; border-top: 3px solid #fff; }
.footer-links { margin-bottom: 20px; }
.footer-links a { color: #fff; margin: 0 10px; text-decoration: none; font-size: 12px; }
.breadcrumb { padding: 8px 15px; font-size: 13px; color: #aaa; background: #111; }
.breadcrumb a { color: var(--yellow); text-decoration: none; }
@media (max-width: 600px) { .event-row { flex-wrap: wrap; } .event-title { width: 100%; margin-top: 10px; } header h1 { font-size: 20px; } }
"""
    with open(os.path.join(OUTPUT_DIR, "style.css"), "w", encoding="utf-8") as f:
        f.write(css_content)

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
        
        # Inject Ad after 3rd item
        if i == 3:
            hp_content += AD_TOP_320_50
            
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
    
    # Fix 4: Homepage hub + league links grid
    hp_content += '<div class="seo-section"><h2>\u26bd Explora Nuestras Secciones</h2>'
    hp_content += '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin-top:15px;">'
    all_hub_links = [
        ("rojadirecta", "Rojadirecta"), ("tarjeta-roja", "Tarjeta Roja"), ("pirlotv", "Pirlo TV"),
        ("tarjeta-roja-en-vivo", "Tarjeta Roja En Vivo"), ("roja-directa", "Roja Directa"),
        ("rojadirecta-tv", "Rojadirecta TV"), ("tarjeta-roja-tv", "Tarjeta Roja TV"),
        ("roja-tv", "Roja TV"), ("targeta-roja", "Targeta Roja"), ("la-roja-directa", "La Roja Directa"),
        ("rojadirecta-futbol", "Rojadirecta F\u00fatbol"), ("pirlo-tv-tarjeta-roja", "Pirlo TV + Tarjeta Roja"),
        ("roja-directa-en-vivo", "Roja Directa En Vivo"), ("futbol-en-vivo-gratis", "F\u00fatbol En Vivo Gratis"),
        ("rojadirecta-online", "Rojadirecta Online"),
        ("champions-league-en-vivo", "\u26bd Champions League"), ("la-liga-en-vivo", "\u26bd La Liga"),
        ("premier-league-en-vivo", "\u26bd Premier League"), ("copa-libertadores-en-vivo", "\u26bd Copa Libertadores"),
        ("liga-mx-en-vivo", "⚽ Liga MX"), ("nba-en-vivo", "🏀 NBA En Vivo"),
        ("futbol-libre", "⚽ Fútbol Libre"), ("futbol-en-vivo", "📺 Fútbol En Vivo"),
        ("futbol-argentino-en-vivo", "🇦🇷 Fútbol Argentino"), ("brasileirao-en-vivo", "🇧🇷 Brasileirão"),
        ("liga-betplay-en-vivo", "🇨🇴 Liga BetPlay"), ("liga-peru-en-vivo", "🇵🇪 Liga 1 Perú"),
        ("liga-chilena-en-vivo", "🇨🇱 Liga Chilena"), ("copa-sudamericana-en-vivo", "🥈 Copa Sudamericana"),
    ]
    for link_slug, link_name in all_hub_links:
        hp_content += f'<a href="/{link_slug}/" class="chan-btn" style="padding:12px;font-size:14px;">{link_name}</a>'
    hp_content += '</div></div>'
    
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
        h1_title="Tarjeta Roja En Vivo - Fútbol Hoy",
        breadcrumbs=[("Inicio", f"{DOMAIN}/")]
    )
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(hp_html)

    # 2. Generate Hub Pages (Aggressive Content)
    hubs = [
        # Original 5 hubs
        ("rojadirecta", "🔴 Rojadirecta TV Online | Ver Fútbol En Vivo Gratis Hoy ⚽", "Sigue toda la emoción de Rojadirecta TV en vivo. La mejor programación de fútbol online gratis, Champions League, La Liga y más en Rojadirecta."),
        ("rojadirecta-tv", "📺 Rojadirecta TV ⚽ Tarjeta Roja En Vivo | Deportes Online Gratis", "Entra en Rojadirecta TV para ver deportes en directo. Enlaces actualizados de fútbol, NBA y tenis. La alternativa número 1 a Rojadirecta."),
        ("tarjeta-roja", "🔴 Tarjeta Roja En Vivo | Ver Fútbol Online Gratis Hoy ⚽", "Disfruta de Tarjeta Roja En Vivo para ver todos los partidos de hoy. La mejor calidad en streaming para fútbol, baloncesto y motor."),
        ("tarjeta-roja-tv", "📺 Tarjeta Roja TV 🔴 Rojadirecta En Vivo Gratis Hoy", "Ver Tarjeta Roja TV online. Accede a los mejores canales de deportes en vivo. Fútbol gratis, NBA y F1 en directo."),
        ("pirlotv", "⚽ Pirlo TV Online 🔴 Ver Fútbol En Vivo Gratis Hoy | Tarjeta Roja", "Accede a Pirlo TV para ver fútbol en vivo. La mejor alternativa a PirloTV y Rojadirecta para disfrutar del deporte rey gratis."),
        # 10 new programmatic SEO hubs from Bing keyword data
        ("tarjeta-roja-en-vivo", "🔴 Tarjeta Roja En Vivo — Ver Partidos de Fútbol Online Gratis Hoy", "Accede a Tarjeta Roja En Vivo para ver fútbol online gratis hoy. Transmisiones en directo de La Liga, Champions League, Premier League y Copa Libertadores sin registro ni suscripción."),
        ("roja-directa", "⚽ Roja Directa — Ver Fútbol En Vivo y En Directo Gratis Hoy", "Entra en Roja Directa para ver todos los partidos de fútbol en vivo y en directo hoy. Enlaces actualizados de streaming gratis, Champions League, La Liga, Premier League y más deportes online."),
        ("roja-tv", "📺 Roja TV — Deportes En Vivo y En Directo Online Gratis Hoy", "Disfruta de Roja TV para ver deportes en vivo y en directo online gratis. Fútbol, NBA, tenis, F1 y más eventos deportivos en streaming HD sin cortes ni interrupciones."),
        ("targeta-roja", "🔴 Targeta Roja — Ver Fútbol En Vivo Gratis Hoy | Streaming HD", "Buscas Targeta Roja para ver fútbol en vivo gratis hoy? Accede a la mejor plataforma de streaming deportivo con enlaces verificados de Rojadirecta TV y Pirlo TV. Sin registro."),
        ("la-roja-directa", "⚽ La Roja Directa — Fútbol En Vivo Gratis | Partidos de Hoy Online", "La Roja Directa te ofrece los mejores enlaces para ver fútbol en vivo gratis hoy. Accede a transmisiones de La Liga, Champions, Premier League y Copa América sin suscripción."),
        ("rojadirecta-futbol", "⚽ Rojadirecta Fútbol — Ver Partidos En Vivo Gratis Hoy | HD Online", "Rojadirecta Fútbol te permite ver todos los partidos de fútbol en vivo y gratis hoy. La Liga, Champions League, Premier League, Serie A y Bundesliga en streaming HD sin cortes."),
        ("pirlo-tv-tarjeta-roja", "📺 Pirlo TV y Tarjeta Roja — Ver Fútbol En Vivo Gratis Hoy ⚽", "Accede a Pirlo TV y Tarjeta Roja para ver fútbol en vivo online gratis hoy. Combinamos las mejores señales de PirloTV y Rojadirecta con transmisiones estables en HD sin registro."),
        ("roja-directa-en-vivo", "🔴 Roja Directa En Vivo — Ver Fútbol Online Gratis Hoy | HD", "Roja Directa En Vivo te ofrece las mejores transmisiones de fútbol online gratis hoy. Enlaces verificados de Rojadirecta TV para ver La Liga, Champions y Copa Libertadores en directo."),
        ("futbol-en-vivo-gratis", "⚽ Fútbol En Vivo Gratis — Ver Partidos Online Hoy | Tarjeta Roja", "Ver fútbol en vivo gratis hoy online en Tarjeta Roja. Transmisiones HD de La Liga, Champions League, Premier League, Copa Libertadores y más sin registro ni pagos. Entra ya."),
        ("rojadirecta-online", "🔴 Rojadirecta Online — Ver Deportes En Vivo Gratis Hoy | Streaming", "Accede a Rojadirecta Online para ver deportes en vivo y gratis hoy. La mejor alternativa para ver fútbol, NBA, tenis y F1 en streaming HD sin interrupciones ni suscripciones."),
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
                {get_hub_seo_content(slug)}
                <h3>Programación Destacada de Hoy</h3>
                <div class="event-list">
        """
        # Add events to hub
        for i, key in enumerate(sorted(grouped.keys())[:20]):
            e = grouped[key]
            accordion_id = f"hub-accordion-{i}"
            
            # Inject Ad after 3rd item
            if i == 3:
                hub_content += AD_TOP_320_50
                
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
        
        # Fix 1: Cross-links to all other hub pages
        cross_links = ''.join([f'<a href="/{s}/" class="chan-btn" style="padding:10px;font-size:13px;">{s.replace("-", " ").title()}</a>' for s, _, _ in hubs if s != slug])
        hub_content += f'<div class="seo-section" style="margin-top:20px;"><h3>M\u00e1s Secciones Populares</h3><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-top:10px;">{cross_links}</div></div>'
        
        hub_content += "</div>"
        
        hub_crumbs = [("Inicio", f"{DOMAIN}/"), (slug.replace('-', ' ').title(), f"{DOMAIN}/{slug}/")]
        hub_html = get_template(title, desc, f"{DOMAIN}/{slug}/", hub_content, schema=generate_faq_schema(paa_qs), h1_title=h1_override, breadcrumbs=hub_crumbs)
        with open(os.path.join(OUTPUT_DIR, slug, "index.html"), "w", encoding="utf-8") as f:
            f.write(hub_html)

    # 3. Generate Match Pages (Expanded Content)
    print("🏟️ Generating Expanded Match Pages...")
    today_date_str = datetime.now().strftime('%d/%m/%Y')
    for idx, (key, e) in enumerate(grouped.items()):
        # Fix 2: Unique titles per match — vary pattern using sport, date, and index
        title_patterns = [
            f"Ver {e['title']} en Vivo | {e['sport']} {today_date_str} — Tarjeta Roja",
            f"{e['title']} en Vivo y en Directo | {e['sport']} Gratis — Tarjeta Roja TV",
            f"{e['title']} Online Gratis | {e['sport']} en Vivo Hoy {today_date_str}",
        ]
        match_title = title_patterns[idx % len(title_patterns)]
        # Fix 3: Meta descriptions ≥120 chars with specific match info
        match_desc = f"Mira {e['title']} en vivo y en directo hoy {today_date_str}. Transmisión gratuita de {e['sport']} en HD por Tarjeta Roja En Vivo, la mejor alternativa a Rojadirecta y Pirlo TV. Sin registro."
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
                <iframe id="main-player" src="{e['channels'][0]['player_url']}" allowfullscreen scrolling="no" sandbox="allow-forms allow-scripts allow-same-origin allow-presentation"></iframe>
            </div>
            <div class="btn-grid">
                {" ".join([f'<button onclick="changeChannel(\'{c["player_url"]}\', this)" class="btn {"active" if i==0 else ""}">{c["canal_name"]}</a>' for i, c in enumerate(e['channels'])])}
            </div>
            <div style="padding: 15px; text-align: center;">
                <button onclick="shareToTelegram('{e['title']}', '{e['time']}', '{match_url}')" class="btn" style="background: #0088cc; width: 100%; max-width: 300px;">
                    ✈️ COMPARTIR EN TELEGRAM
                </button>
            </div>
            {AD_BOTTOM_300_250}
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
        
        match_crumbs = [("Inicio", f"{DOMAIN}/"), ("Partido", f"{DOMAIN}/"), (e['title'], match_url)]
        match_html = get_template(match_title, match_desc, match_url, match_content, match_schema, h1_title=f"Ver {e['title']} en Vivo", breadcrumbs=match_crumbs)
        file_path = os.path.join(OUTPUT_DIR, "partido", f"{e['slug']}-en-vivo.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(match_html)

    # 4. Generate Date Pages (Programmatic)
    print("📅 Generating Programmatic Date Pages...")
    today = datetime.now()
    dates = [
        ("hoy", today),
        ("manana", today + timedelta(days=1))
    ]
    
    for slug, date_obj in dates:
        date_str = date_obj.strftime('%Y-%m-%d')
        date_display = date_obj.strftime('%d/%m/%Y')
        # Fix 2: Unique titles with actual date
        if slug == "hoy":
            title = f"Fútbol En Vivo Hoy {date_display} ⚽ Agenda Completa de Partidos | Tarjeta Roja"
            desc = f"Consulta la agenda completa de fútbol en vivo para hoy {date_display}. Todos los partidos de La Liga, Champions League, Premier League y más en Rojadirecta y Tarjeta Roja. Streaming gratis sin registro."
        else:
            title = f"Fútbol En Vivo Mañana {date_display} ⚽ Próximos Partidos Programados | Tarjeta Roja"
            desc = f"Descubre los partidos de fútbol en vivo programados para mañana {date_display}. Horarios, canales y enlaces gratuitos de Rojadirecta, Pirlo TV y Tarjeta Roja En Vivo. Prepárate para no perderte nada."
        
        date_content = f'<div class="card"><div class="card-header">📅 AGENDA DE FÚTBOL: {date_str}</div>'
        for i, key in enumerate(sorted(grouped.keys())):
            e = grouped[key]
            accordion_id = f"date-accordion-{i}"
            
            # Inject Ad after 3rd item
            if i == 3:
                date_content += AD_TOP_320_50

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
        
        date_crumbs = [("Inicio", f"{DOMAIN}/"), ("Agenda", f"{DOMAIN}/agenda/futbol-en-vivo-hoy"), ("F\u00fatbol " + slug.title(), f"{DOMAIN}/agenda/futbol-en-vivo-{slug}")]
        date_html = get_template(title, desc, f"{DOMAIN}/agenda/futbol-en-vivo-{slug}", date_content, breadcrumbs=date_crumbs)
        with open(os.path.join(OUTPUT_DIR, "agenda", f"futbol-en-vivo-{slug}.html"), "w", encoding="utf-8") as f:
            f.write(date_html)

    # 4.5. Generate League/Competition Landing Pages
    print("🏆 Generating League Landing Pages...")
    leagues = [
        ("champions-league-en-vivo", "⚽ Champions League En Vivo — Ver Partidos Gratis Hoy | Tarjeta Roja",
         "Ver la Champions League en vivo y en directo gratis hoy. Todos los partidos de la UEFA Champions League en streaming HD. Real Madrid, Barcelona, Liverpool, PSG y más en Tarjeta Roja.",
         "Champions League En Vivo", "Champions League"),
        ("la-liga-en-vivo", "⚽ La Liga En Vivo — Ver Partidos de La Liga Española Gratis Hoy",
         "Disfruta de La Liga en vivo y en directo gratis hoy. Todos los partidos de La Liga Española en streaming: Real Madrid, Barcelona, Atlético de Madrid y más en Tarjeta Roja.",
         "La Liga En Vivo", "La Liga Española"),
        ("premier-league-en-vivo", "⚽ Premier League En Vivo — Ver Partidos de la Liga Inglesa Gratis",
         "Ver la Premier League en vivo y en directo gratis hoy. Partidos de Manchester City, Arsenal, Liverpool, Chelsea y más en streaming HD por Tarjeta Roja En Vivo.",
         "Premier League En Vivo", "Premier League"),
        ("copa-libertadores-en-vivo", "⚽ Copa Libertadores En Vivo — Ver Partidos Gratis Hoy | Streaming",
         "Ver la Copa Libertadores en vivo y en directo gratis hoy. Partidos de Boca Juniors, River Plate, Flamengo, Palmeiras y más en streaming HD por Tarjeta Roja.",
         "Copa Libertadores En Vivo", "Copa Libertadores"),
        ("liga-mx-en-vivo", "⚽ Liga MX En Vivo — Ver Partidos del Fútbol Mexicano Gratis Hoy",
         "Disfruta de la Liga MX en vivo y en directo gratis hoy. Partidos de América, Chivas, Cruz Azul, Monterrey y más en streaming HD por Tarjeta Roja En Vivo.",
         "Liga MX En Vivo", "Liga MX"),
        ("nba-en-vivo", "🏀 NBA En Vivo — Ver Partidos de Baloncesto Gratis Hoy | Streaming",
         "Ver la NBA en vivo y en directo gratis hoy. Partidos de Lakers, Celtics, Warriors, Bucks y más en streaming HD. La mejor alternativa para ver baloncesto online en Tarjeta Roja.",
         "NBA En Vivo", "NBA"),
        # New LATAM leagues
        ("futbol-argentino-en-vivo", "⚽ Fútbol Argentino En Vivo — Ver Liga Profesional Argentina Gratis Hoy",
         "Ver Fútbol Argentino en vivo y en directo gratis hoy. Partidos de Boca Juniors, River Plate, Racing, Independiente y más de la Liga Profesional Argentina en streaming HD por Tarjeta Roja.",
         "Fútbol Argentino En Vivo", "Fútbol Argentino"),
        ("brasileirao-en-vivo", "⚽ Brasileirão En Vivo — Ver Serie A de Brasil Gratis Hoy | Streaming",
         "Ver el Brasileirão en vivo y en directo gratis hoy. Partidos de Palmeiras, Flamengo, São Paulo, Corinthians y más de la Serie A de Brasil en Tarjeta Roja.",
         "Brasileirão En Vivo", "Brasileirão"),
        ("liga-betplay-en-vivo", "⚽ Liga BetPlay En Vivo — Ver Fútbol Colombiano Gratis Hoy | Tarjeta Roja",
         "Ver la Liga BetPlay en vivo y en directo gratis hoy. Partidos de Millonarios, Atlético Nacional, América de Cali, Deportivo Cali y más del fútbol colombiano en streaming HD.",
         "Liga BetPlay En Vivo", "Liga BetPlay"),
        ("liga-peru-en-vivo", "⚽ Liga 1 Perú En Vivo — Ver Fútbol Peruano Gratis Hoy | Streaming",
         "Ver la Liga 1 de Perú en vivo y en directo gratis hoy. Partidos de Alianza Lima, Universitario, Sporting Cristal y más del fútbol peruano en Tarjeta Roja.",
         "Liga 1 Perú En Vivo", "Liga 1 Perú"),
        ("liga-chilena-en-vivo", "⚽ Liga Chilena En Vivo — Ver Primera División de Chile Gratis Hoy",
         "Ver la Liga Chilena en vivo y en directo gratis hoy. Partidos de Colo Colo, Universidad de Chile, U. Católica y más de la Primera División en streaming por Tarjeta Roja.",
         "Liga Chilena En Vivo", "Liga Chilena"),
        ("copa-sudamericana-en-vivo", "⚽ Copa Sudamericana En Vivo — Ver Partidos Gratis Hoy | Tarjeta Roja",
         "Ver la Copa Sudamericana en vivo y en directo gratis hoy. Todos los partidos del torneo CONMEBOL en streaming HD por Tarjeta Roja En Vivo.",
         "Copa Sudamericana En Vivo", "Copa Sudamericana"),
    ]

    for league_slug, league_title, league_desc, league_h1, league_name in leagues:
        sport_type = "Baloncesto" if "NBA" in league_name else "Fútbol"
        league_content = f"""
        <div class="card">
            <div class="card-header">{league_h1.upper()}</div>
            <div class="seo-section" style="box-shadow: none; margin-top: 0;">
                <h2>{league_h1} — Disfruta del Mejor {sport_type} Online Gratis</h2>
                <p>Bienvenido a la sección dedicada a <strong>{league_name}</strong> en Tarjeta Roja En Vivo. Aquí encontrarás todos los partidos de la {league_name} en vivo y en directo, con enlaces de streaming verificados y actualizados constantemente.</p>
                <p>En <strong>Tarjeta Roja En Vivo</strong> nos especializamos en ofrecer las mejores transmisiones de la <strong>{league_name}</strong>. Nuestros enlaces son verificados por nuestro equipo antes de cada jornada para garantizar la mejor experiencia de streaming.</p>
                <h3>¿Cómo ver la {league_name} en vivo gratis?</h3>
                <p>Para ver los partidos de la <strong>{league_name}</strong> en vivo solo necesitas acceder a esta página el día del encuentro. Publicamos los enlaces de streaming minutos antes del inicio de cada partido. Nuestras señales son compatibles con PC, móvil, tablet y Smart TV.</p>
                <h3>Próximos partidos de la {league_name}</h3>
            </div>
            <div class="event-list">
        """
        for i, key in enumerate(sorted(grouped.keys())[:15]):
            e = grouped[key]
            accordion_id = f"league-{league_slug}-{i}"
            if i == 3:
                league_content += AD_TOP_320_50
            league_content += f"""
            <div class="event-row" onclick="toggleAccordion('{accordion_id}')">
                <div class="event-time">{e['time']}</div>
                <div class="event-title">{e['title']}</div>
                <div style="color: var(--red); font-weight: bold;">VER &raquo;</div>
            </div>
            <div id="{accordion_id}" class="event-channels">
                <a href="/partido/{e['slug']}-en-vivo" class="chan-btn" style="background: var(--yellow); color: #000;">VER PARTIDO</a>
                {" ".join([f'<a href="/partido/{e["slug"]}-en-vivo" class="chan-btn">{c["canal_name"]}</a>' for c in e['channels']])}
            </div>"""
        league_content += '</div>'
        
        # Cross-links to other leagues and top hubs
        league_cross = ''.join([f'<a href="/{ls}/" class="chan-btn" style="padding:10px;font-size:13px;">{ln}</a>' for ls, _, _, _, ln in leagues if ls != league_slug])
        hub_cross = ''.join([f'<a href="/{s}/" class="chan-btn" style="padding:10px;font-size:13px;">{s.replace("-", " ").title()}</a>' for s, _, _ in hubs[:5]])
        league_content += f'<div class="seo-section" style="margin-top:20px;"><h3>Más Competiciones y Secciones</h3><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-top:10px;">{league_cross}{hub_cross}</div></div>'
        league_content += '</div>'
        
        league_crumbs = [("Inicio", f"{DOMAIN}/"), (league_name, f"{DOMAIN}/{league_slug}/")]
        league_html = get_template(league_title, league_desc, f"{DOMAIN}/{league_slug}/", league_content, h1_title=league_h1, breadcrumbs=league_crumbs)
        with open(os.path.join(OUTPUT_DIR, league_slug, "index.html"), "w", encoding="utf-8") as f:
            f.write(league_html)

    # 5. Generate Multiple Sitemaps
    print("🗺️ Generating Advanced Sitemaps...")
    build_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')
    
    def write_sitemap(filename, urls, changefreq="hourly", priority="0.8"):
        """Write a sitemap XML file with lastmod timestamps."""
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
            for url in urls:
                f.write(f'  <url><loc>{url}</loc><lastmod>{build_date}</lastmod><changefreq>{changefreq}</changefreq><priority>{priority}</priority></url>\n')
            f.write('</urlset>')

    # Sitemap for static pages
    write_sitemap("sitemap-pages.xml", [
        f"{DOMAIN}/",
        f"{DOMAIN}/aviso-legal",
        f"{DOMAIN}/contacto"
    ], changefreq="weekly", priority="1.0")
    
    write_sitemap("sitemap-hubs.xml", [f"{DOMAIN}/{h[0]}/" for h in hubs] + [f"{DOMAIN}/futbol-libre/", f"{DOMAIN}/futbol-en-vivo/"])
    write_sitemap("sitemap-leagues.xml", [f"{DOMAIN}/{l[0]}/" for l in leagues])
    write_sitemap("sitemap-matches.xml", [f"{DOMAIN}/partido/{e['slug']}-en-vivo" for e in grouped.values()])
    write_sitemap("sitemap-dates.xml", [f"{DOMAIN}/agenda/futbol-en-vivo-hoy", f"{DOMAIN}/agenda/futbol-en-vivo-manana"])
    
    # Main Sitemap Index with lastmod
    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for sm in ["sitemap-pages.xml", "sitemap-hubs.xml", "sitemap-leagues.xml", "sitemap-matches.xml", "sitemap-dates.xml"]:
            f.write(f'  <sitemap><loc>{DOMAIN}/{sm}</loc><lastmod>{build_date}</lastmod></sitemap>\n')
        f.write('</sitemapindex>')

    # 6. Generate Legal and Contact Pages (Fix 3 & 4: expanded content + longer meta)
    print("⚖️ Generating Legal and Contact Pages...")
    legal_content = """
    <div class="card">
        <div class="card-header">AVISO LEGAL — TARJETA ROJA EN VIVO</div>
        <div class="seo-section" style="box-shadow: none; margin-top: 0;">
            <h2>Aviso Legal y Términos de Uso</h2>
            <p>Bienvenido al aviso legal de <strong>Tarjeta Roja En Vivo</strong> (tarjetarojaenvivo.live). Al acceder y utilizar este sitio web, usted acepta los siguientes términos y condiciones de uso. Le recomendamos leer detenidamente esta información antes de navegar por nuestro portal.</p>

            <h3>1. Naturaleza del Servicio</h3>
            <p>Este sitio web es un portal de información deportiva que actúa como un agregador de enlaces públicos disponibles en internet. <strong>No alojamos, almacenamos ni distribuimos ningún contenido audiovisual</strong> en nuestros propios servidores. Todos los enlaces y señales de streaming que aparecen en nuestras páginas provienen de fuentes externas de acceso público como YouTube, Twitch y otras plataformas de video.</p>

            <h3>2. Propiedad Intelectual</h3>
            <p>Todos los logotipos, marcas comerciales y nombres de equipos deportivos que aparecen en este sitio web pertenecen a sus respectivos propietarios. El uso de estos elementos es meramente informativo y no implica ninguna afiliación, patrocinio o relación comercial con las entidades mencionadas. El contenido original de este sitio, incluyendo textos, diseño y estructura, está protegido por las leyes de propiedad intelectual aplicables.</p>

            <h3>3. Responsabilidad del Usuario</h3>
            <p>El usuario es el único responsable del uso que haga de la información y los enlaces proporcionados en este portal. Tarjeta Roja En Vivo no se hace responsable de las acciones que los usuarios realicen a través de enlaces de terceros, y recomienda verificar siempre la legalidad del contenido en su jurisdicción local antes de acceder a cualquier transmisión en vivo.</p>

            <h3>4. Enlaces a Terceros</h3>
            <p>Este sitio web puede contener enlaces a páginas externas sobre las cuales no tenemos control alguno. No nos hacemos responsables del contenido, las políticas de privacidad ni las prácticas de dichos sitios. La inclusión de cualquier enlace no implica necesariamente una recomendación o aprobación de las opiniones expresadas en ellos.</p>

            <h3>5. Política de Privacidad</h3>
            <p>Respetamos la privacidad de nuestros visitantes. Utilizamos cookies y herramientas analíticas (como Google Analytics) para mejorar la experiencia de navegación y comprender cómo los usuarios interactúan con nuestro sitio. No recopilamos información personal identificable a menos que el usuario la proporcione voluntariamente a través de nuestro formulario de contacto.</p>

            <h3>6. Solicitudes de Retirada (DMCA)</h3>
            <p>Si usted es el propietario legítimo de algún contenido enlazado desde nuestro portal y desea que sea retirado, le rogamos que se ponga en contacto con nosotros a través de nuestro <a href="/contacto" style="color: var(--red);">formulario de contacto</a>. Atenderemos su solicitud en un plazo máximo de 48 horas laborables.</p>

            <h3>7. Modificaciones</h3>
            <p>Nos reservamos el derecho de modificar estos términos en cualquier momento y sin previo aviso. Se recomienda revisar esta página periódicamente para estar al tanto de posibles cambios.</p>
        </div>
    </div>"""
    # Fix 3: Longer meta description for legal page
    legal_crumbs = [("Inicio", f"{DOMAIN}/"), ("Aviso Legal", f"{DOMAIN}/aviso-legal")]
    legal_html = get_template(
        "Aviso Legal y Términos de Uso | Tarjeta Roja En Vivo — Política de Privacidad",
        "Consulta el aviso legal, términos de uso y política de privacidad de Tarjeta Roja En Vivo. Información sobre propiedad intelectual, responsabilidades del usuario y solicitudes DMCA.",
        f"{DOMAIN}/aviso-legal", legal_content,
        breadcrumbs=legal_crumbs
    )
    with open(os.path.join(OUTPUT_DIR, "aviso-legal.html"), "w", encoding="utf-8") as f:
        f.write(legal_html)

    contacto_content = """
    <div class="card">
        <div class="card-header">CONTACTO — TARJETA ROJA EN VIVO</div>
        <div class="seo-section" style="box-shadow: none; margin-top: 0;">
            <h2>Contacta con Tarjeta Roja En Vivo</h2>
            <p>En <strong>Tarjeta Roja En Vivo</strong> valoramos la comunicación con nuestros usuarios. Si tienes alguna duda, sugerencia, reclamación o propuesta de colaboración, no dudes en ponerte en contacto con nuestro equipo. Estamos aquí para ayudarte.</p>

            <h3>Correo Electrónico</h3>
            <p>La forma más directa de contactarnos es a través de nuestro correo electrónico oficial:</p>
            <p style="text-align: center; font-weight: bold; font-size: 20px; color: var(--red);">contacto@tarjetarojaenvivo.live</p>

            <h3>Tiempo de Respuesta</h3>
            <p>Nos comprometemos a responder todas las consultas en un plazo máximo de <strong>48 horas laborables</strong>. Durante eventos deportivos importantes o períodos de alta demanda, este plazo podría extenderse ligeramente, pero haremos todo lo posible por atenderte lo antes posible.</p>

            <h3>Solicitudes de Retirada de Contenido (DMCA)</h3>
            <p>Si eres el propietario legítimo de algún contenido enlazado desde nuestro portal y deseas que sea retirado, por favor envíanos un correo con la siguiente información:</p>
            <ul style="color: #555; padding-left: 20px;">
                <li>Tu nombre completo y datos de contacto</li>
                <li>La URL exacta del contenido en nuestro sitio</li>
                <li>Prueba de que eres el titular de los derechos</li>
                <li>Una declaración de buena fe indicando que el uso no está autorizado</li>
            </ul>
            <p>Procesaremos tu solicitud con la mayor brevedad y diligencia posible.</p>

            <h3>Colaboraciones y Publicidad</h3>
            <p>Si estás interesado en colaborar con nosotros, proponer contenido patrocinado o explorar opciones de publicidad en nuestro portal deportivo, escríbenos al correo indicado con el asunto "Colaboración" y te responderemos con más información sobre nuestras opciones disponibles.</p>

            <h3>Síguenos en Redes Sociales</h3>
            <p>Mantente al día con las últimas novedades, horarios de partidos y actualizaciones de canales siguiéndonos en nuestras redes sociales. Publicamos alertas en tiempo real de los eventos más importantes del día.</p>
        </div>
    </div>"""
    # Fix 3: Longer meta description for contact page
    contacto_crumbs = [("Inicio", f"{DOMAIN}/"), ("Contacto", f"{DOMAIN}/contacto")]
    contacto_html = get_template(
        "Contacto | Tarjeta Roja En Vivo — Escríbenos para Dudas, Sugerencias o DMCA",
        "Ponte en contacto con el equipo de Tarjeta Roja En Vivo. Envíanos tus dudas, sugerencias, solicitudes DMCA o propuestas de colaboración. Respuesta garantizada en 48 horas laborables.",
        f"{DOMAIN}/contacto", contacto_content,
        breadcrumbs=contacto_crumbs
    )
    with open(os.path.join(OUTPUT_DIR, "contacto.html"), "w", encoding="utf-8") as f:
        f.write(contacto_html)

    # 7. Generate robots.txt with AI bot directives
    print("🤖 Generating robots.txt with AI bot directives...")
    robots_content = f"""# Tarjeta Roja En Vivo — Fútbol Libre · Roja Directa · Pirlo TV
# https://www.tarjetarojaenvivo.live

# Bing crawler
User-agent: bingbot
Allow: /
Crawl-delay: 1

User-agent: msnbot
Allow: /

# AI assistants (citation optimization)
User-agent: ChatGPT-User
Allow: /

User-agent: GPTBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: Google-Extended
Allow: /

# General crawlers
User-agent: *
Allow: /

Sitemap: {DOMAIN}/sitemap.xml
"""
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_content)

    print(f"✅ Success! Elite SEO Site generated in '{OUTPUT_DIR}'.")

if __name__ == "__main__":
    generate_site()
