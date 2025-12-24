import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';

const MatchDetail = () => {
    const { slug } = useParams();
    const [match, setMatch] = useState(null);
    const [loading, setLoading] = useState(true);
    const [showShield, setShowShield] = useState(true);
    const [activeChannel, setActiveChannel] = useState(null);

    useEffect(() => {
        // 🛡 AGENT 14 — MOBILE POPUP & REDIRECT DEFENSE ENGINE
        const noop = () => { };
        const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

        // 1. JS API INTERCEPTION
        const originalOpen = window.open;
        window.open = function () { return { focus: noop, close: noop, closed: true }; };

        // 2. DIALOG & EXIT-TRAP NEUTRALIZATION
        const originalAlert = window.alert;
        const originalConfirm = window.confirm;
        const originalPrompt = window.prompt;
        window.alert = noop;
        window.confirm = noop;
        window.prompt = noop;
        const originalBeforeUnload = window.onbeforeunload;
        window.onbeforeunload = null;

        // 3. RUNTIME SCRIPT INJECTION BLOCKING
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.tagName === 'SCRIPT') {
                        const src = node.src || '';
                        if (src && !src.includes(window.location.hostname) && !src.includes('google') && !src.includes('cloudflare')) {
                            node.remove();
                        }
                    }
                    if (node.tagName === 'IFRAME' && !node.id?.includes('main-player')) {
                        node.remove();
                    }
                });
            });
        });
        observer.observe(document.documentElement, { childList: true, subtree: true });

        // 4. MOBILE TAP & CLICK HIJACK DEFENSE
        const clickHandler = (e) => {
            if (e.target.tagName === 'BODY' || e.target.tagName === 'HTML') {
                e.preventDefault();
                e.stopPropagation();
            }
        };
        document.addEventListener('click', clickHandler, true);

        const touchHandler = (e) => {
            const target = document.elementFromPoint(e.touches[0].clientX, e.touches[0].clientY);
            if (target && (target.tagName === 'BODY' || target.tagName === 'HTML')) {
                e.preventDefault();
            }
        };
        if (isMobile) {
            document.addEventListener('touchstart', touchHandler, { passive: false });
        }

        // 5. Block postMessage abuse
        const messageHandler = (e) => {
            if (e.data && typeof e.data === 'string' && (e.data.includes('open') || e.data.includes('popup'))) {
                e.stopImmediatePropagation();
            }
        };
        window.addEventListener('message', messageHandler, true);

        return () => {
            window.open = originalOpen;
            window.alert = originalAlert;
            window.confirm = originalConfirm;
            window.prompt = originalPrompt;
            window.onbeforeunload = originalBeforeUnload;
            document.removeEventListener('click', clickHandler, true);
            if (isMobile) document.removeEventListener('touchstart', touchHandler);
            window.removeEventListener('message', messageHandler, true);
            observer.disconnect();
        };
    }, []);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('https://raw.githubusercontent.com/albinchristo04/tarjetarojaenvivoo/refs/heads/main/results/player_urls_latest.json');
                const data = await response.json();

                // Find the match by slug
                const foundMatch = data.events.find(event => {
                    const eventSlug = event.event_title.toLowerCase().replace(/[^a-z0-9]+/g, '-');
                    return eventSlug === slug;
                });

                if (foundMatch) {
                    // Group channels for this match
                    const channels = data.events.filter(e => e.event_title === foundMatch.event_title && e.event_time === foundMatch.event_time);
                    setMatch({
                        ...foundMatch,
                        channels: channels
                    });
                    // Set default channel
                    if (channels.length > 0) {
                        setActiveChannel(channels[0]);
                    }
                }
                setLoading(false);
            } catch (error) {
                console.error('Error fetching match details:', error);
                setLoading(false);
            }
        };

        fetchData();
    }, [slug]);

    const handleChannelChange = (channel) => {
        setActiveChannel(channel);
        setShowShield(true);
    };

    if (loading) {
        return <div style={{ color: 'white', textAlign: 'center', marginTop: '50px' }}>Cargando evento...</div>;
    }

    if (!match) {
        return (
            <div style={{ color: 'white', textAlign: 'center', marginTop: '50px' }}>
                <h2>Evento no encontrado</h2>
                <Link to="/" style={{ color: '#ffcc00' }}>Volver a la programación</Link>
            </div>
        );
    }

    const pageTitle = `Ver ${match.event_title} EN VIVO Online Gratis | Tarjeta Roja`;
    const pageDescription = `Disfruta del partido ${match.event_title} en vivo y gratis. Enlaces de Rojadirecta, Pirlo TV y Tarjeta Roja para ver deportes online.`;

    return (
        <div className="match-detail-container" style={{ maxWidth: '1000px', margin: '20px auto', padding: '0 10px' }}>
            <Helmet>
                <title>{pageTitle}</title>
                <meta name="description" content={pageDescription} />
                <meta property="og:title" content={pageTitle} />
                <meta property="og:description" content={pageDescription} />
                <link rel="canonical" href={`https://www.tarjetarojaenvivo.live/ver/${slug}`} />
                <script type="application/ld+json">
                    {JSON.stringify({
                        "@context": "https://schema.org",
                        "@type": "SportsEvent",
                        "name": match.event_title,
                        "description": pageDescription,
                        "startDate": new Date().toISOString().split('T')[0] + 'T' + match.event_time,
                        "sport": match.sport,
                        "location": {
                            "@type": "Place",
                            "name": "Online"
                        },
                        "offers": {
                            "@type": "Offer",
                            "url": `https://www.tarjetarojaenvivo.live/ver/${slug}`,
                            "price": "0",
                            "priceCurrency": "USD",
                            "availability": "https://schema.org/InStock"
                        }
                    })}
                </script>
            </Helmet>

            <div className="match-header" style={{ background: '#333', color: '#ffcc00', padding: '20px', textAlign: 'center', borderRadius: '5px 5px 0 0' }}>
                <h1 style={{ margin: '0', fontSize: '24px' }}>{match.event_title}</h1>
                <p style={{ margin: '10px 0 0', color: '#fff' }}>
                    <span style={{ fontWeight: 'bold' }}>Hora:</span> {match.event_time} |
                    <span style={{ fontWeight: 'bold', marginLeft: '10px' }}>Deporte:</span> {match.sport}
                </p>
            </div>

            {/* Player Section with Iframe and Shield */}
            <div className="player-container" style={{ background: '#000', border: '1px solid #333', position: 'relative', overflow: 'hidden', paddingTop: '56.25%', cursor: 'pointer' }}>
                {showShield && (
                    <div
                        className="player-shield"
                        onClick={() => setShowShield(false)}
                        style={{
                            position: 'absolute',
                            top: 0,
                            left: 0,
                            width: '100%',
                            height: '100%',
                            zIndex: 10,
                            background: 'rgba(0,0,0,0.01)',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center'
                        }}
                    >
                        <div className="shield-msg" style={{
                            background: '#d32f2f',
                            color: '#fff',
                            padding: '10px 20px',
                            borderRadius: '30px',
                            fontWeight: 'bold',
                            boxShadow: '0 4px 15px rgba(0,0,0,0.5)'
                        }}>
                            CLIC PARA VER EL PARTIDO
                        </div>
                    </div>
                )}
                {activeChannel ? (
                    <iframe
                        src={activeChannel.player_url}
                        title={activeChannel.canal_name}
                        style={{
                            position: 'absolute',
                            top: 0,
                            left: 0,
                            width: '100%',
                            height: '100%',
                            border: 'none',
                            zIndex: 1
                        }}
                        allowFullScreen
                        scrolling="no"
                    ></iframe>
                ) : (
                    <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', color: '#fff' }}>
                        No hay señal disponible
                    </div>
                )}
            </div>

            <div className="player-controls" style={{ background: '#1a1a1a', padding: '20px', textAlign: 'center', border: '1px solid #333', borderTop: 'none' }}>
                <div style={{ color: '#aaa', marginBottom: '15px', fontSize: '14px' }}>
                    Canales disponibles:
                </div>
                <div className="channel-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))', gap: '10px' }}>
                    {match.channels.map((channel, index) => (
                        <button
                            key={index}
                            onClick={() => handleChannelChange(channel)}
                            style={{
                                background: activeChannel?.canal_name === channel.canal_name ? '#ffcc00' : '#d32f2f',
                                color: activeChannel?.canal_name === channel.canal_name ? '#000' : '#fff',
                                padding: '10px',
                                borderRadius: '4px',
                                fontWeight: 'bold',
                                border: 'none',
                                cursor: 'pointer',
                                transition: 'all 0.3s ease'
                            }}
                        >
                            {channel.canal_name}
                        </button>
                    ))}
                </div>
            </div>

            <div className="seo-content" style={{ background: '#fff', color: '#333', padding: '20px', marginTop: '20px', borderRadius: '0 0 5px 5px', lineHeight: '1.6' }}>
                <h2>Cómo ver {match.event_title} en vivo gratis</h2>
                <p>
                    Bienvenido a <strong>Tarjeta Roja En Vivo</strong>, tu mejor opción para ver <strong>{match.event_title}</strong> online.
                    Ofrecemos múltiples enlaces de alta calidad para que no te pierdas ni un segundo de la acción.
                </p>
                <p>
                    Nuestros enlaces son compatibles con dispositivos móviles, tablets y PC. Si buscas alternativas a
                    <strong> Rojadirecta</strong>, <strong>Pirlo TV</strong> o <strong>Elitegol</strong>, has llegado al lugar indicado.
                </p>
                <h3>Detalles del Evento:</h3>
                <ul>
                    <li><strong>Evento:</strong> {match.event_title}</li>
                    <li><strong>Deporte:</strong> {match.sport}</li>
                    <li><strong>Transmisión:</strong> En Vivo / Directo</li>
                </ul>
                <Link to="/" style={{ display: 'inline-block', marginTop: '20px', color: '#d32f2f', fontWeight: 'bold' }}>
                    ← Volver a la Programación de Hoy
                </Link>
            </div>
        </div>
    );
};

export default MatchDetail;
