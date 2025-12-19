import React, { useState, useEffect } from 'react';

const Schedule = () => {
    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState(true);

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
                            channels: []
                        };
                    }
                    groupedEvents[key].channels.push({
                        name: event.canal_name,
                        url: event.canal_url, // Or player_url depending on what we want to link
                        player_url: event.player_url
                    });
                });

                // Convert to array and sort by time (simple string sort works for HH:MM usually)
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

    if (loading) {
        return <div style={{ color: 'white', textAlign: 'center', marginTop: '20px' }}>Cargando programación...</div>;
    }

    return (
        <div className="schedule-container">
            <div className="schedule-header">
                Programación de Hoy en TARJETA ROJA
            </div>
            <div className="event-list">
                {events.map((event, index) => (
                    <div key={index} className={`event-group ${index % 2 === 0 ? 'alt' : ''}`}>
                        <div className="event-row">
                            <div className="event-time">{event.time}</div>
                            <div className="event-sport">
                                <img src="https://www.tarjetarojaenvivo.club/img/tv.png" alt="TV" style={{ width: '16px', verticalAlign: 'middle' }} />
                            </div>
                            <div className="event-title">
                                {event.title}
                            </div>
                        </div>
                        <div className="channel-list">
                            {event.channels.map((channel, cIndex) => (
                                <div key={cIndex} className="channel-item">
                                    <span className="channel-icon">▶</span>
                                    <a href={channel.url} target="_blank" rel="noopener noreferrer" className="channel-link">
                                        {channel.name}
                                    </a>
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Schedule;
