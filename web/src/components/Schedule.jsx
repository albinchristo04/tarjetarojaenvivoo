import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';

const Schedule = () => {
    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [expandedIndex, setExpandedIndex] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('https://raw.githubusercontent.com/albinchristo04/tarjetarojaenvivoo/refs/heads/main/results/player_urls_latest.json');
                const data = await response.json();

                // Group events by title and time
                const groupedEvents = {};

                data.events.forEach(event => {
                    const key = `${event.event_time}-${event.event_title}`;
                    if (!groupedEvents[key]) {
                        groupedEvents[key] = {
                            title: event.event_title,
                            time: event.event_time,
                            sport: event.sport,
                            slug: event.event_title.toLowerCase().replace(/[^a-z0-9]+/g, '-'),
                            channels: []
                        };
                    }
                    groupedEvents[key].channels.push({
                        name: event.canal_name,
                        url: event.canal_url,
                        player_url: event.player_url
                    });
                });

                const eventsArray = Object.values(groupedEvents).sort((a, b) => a.time.localeCompare(b.time));

                setEvents(eventsArray);
                setLoading(false);
            } catch (error) {
                console.error('Error fetching data:', error);
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    const toggleExpand = (index) => {
        if (expandedIndex === index) {
            setExpandedIndex(null);
        } else {
            setExpandedIndex(index);
        }
    };

    if (loading) {
        return <div style={{ color: 'white', textAlign: 'center', marginTop: '20px' }}>Cargando programación...</div>;
    }

    return (
        <div className="schedule-container">
            <Helmet>
                <title>Tarjeta Roja En Vivo | Rojadirecta TV | Pirlo TV | Fútbol Gratis Online</title>
                <meta name="description" content="Ver fútbol en VIVO en Tarjeta Roja. Agenda de hoy: Real Madrid, Barcelona, NBA, F1. La mejor alternativa a Rojadirecta y Pirlo TV. ¡Entra YA!" />
            </Helmet>

            <div className="schedule-header">
                Programación de Hoy en TARJETA ROJA
            </div>
            <div className="event-list">
                {events.map((event, index) => (
                    <div key={index} className={`event-group ${index % 2 === 0 ? 'alt' : ''}`}>
                        <div
                            className="event-row"
                            onClick={() => toggleExpand(index)}
                            style={{ cursor: 'pointer' }}
                        >
                            <div className="event-time">{event.time}</div>
                            <div className="event-sport">
                                <span style={{ fontSize: '18px', marginRight: '10px' }}>📺</span>
                            </div>
                            <div className="event-title">
                                {event.title}
                            </div>
                            <div style={{ fontSize: '12px', color: '#666' }}>
                                {expandedIndex === index ? '▲' : '▼'}
                            </div>
                        </div>

                        {expandedIndex === index && (
                            <div className="channel-list" style={{ display: 'block' }}>
                                {event.channels.map((channel, cIndex) => (
                                    <div key={cIndex} className="channel-item">
                                        <span className="channel-icon">▶</span>
                                        <Link to={`/ver/${event.slug}`} className="channel-link">
                                            {channel.name}
                                        </Link>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                ))}
            </div>

            {/* SEO Text Block for Homepage */}
            <div style={{ background: '#f9f9f9', color: '#333', padding: '20px', marginTop: '20px', fontSize: '14px', lineHeight: '1.6' }}>
                <h2>¿Qué es Tarjeta Roja En Vivo?</h2>
                <p>
                    <strong>Tarjeta Roja En Vivo</strong> es la plataforma líder para ver deportes por internet de forma gratuita.
                    Somos la evolución de sitios clásicos como <strong>Rojadirecta</strong>, <strong>Pirlo TV</strong> y <strong>Intergoles</strong>.
                    Aquí podrás encontrar la mejor programación de fútbol, baloncesto, tenis, F1 y mucho más.
                </p>
                <h3>Ver Fútbol Online Gratis</h3>
                <p>
                    Si buscas ver los partidos de La Liga, Champions League, Premier League o la Copa Libertadores,
                    nuestra agenda se actualiza diariamente para ofrecerte los mejores enlaces en HD.
                    No necesitas suscripciones costosas para disfrutar de tu pasión.
                </p>
                <ul>
                    <li><strong>Rojadirecta TV:</strong> Los mejores enlaces de la red.</li>
                    <li><strong>Pirlo TV:</strong> Transmisiones estables y rápidas.</li>
                    <li><strong>Tarjeta Roja Directa:</strong> El sitio oficial para los fanáticos.</li>
                </ul>
            </div>
        </div>
    );
};

export default Schedule;
