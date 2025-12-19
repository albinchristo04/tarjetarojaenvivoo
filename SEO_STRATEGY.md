# Estrategia SEO Agresiva para TarjetaRojaEnVivo.live

## 1. Keyword Clustering & Intent Mapping

**Cluster A: Brand Hijacking (High Volume)**
*   *Keywords*: rojadirecta, tarjeta roja, rojadirecta tv, tarjeta roja tv, pirlotv, pirlo tv rojadirecta.
*   *Intent*: Navigational/Transactional. Users want the specific "look and feel" and immediate links.
*   *Strategy*: Exact match titles, "Clone" aesthetics (already done), aggressive H1 usage.

**Cluster B: "En Vivo" Generic (Medium Volume)**
*   *Keywords*: futbol en vivo, ver partidos gratis, deportes online, tarjeta roja futbol en vivo.
*   *Intent*: Informational/Transactional.
*   *Strategy*: Category pages (e.g., /futbol/, /nba/) and "Agenda" style content.

**Cluster C: Match Specific (Long-Tail / Programmatic)**
*   *Keywords*: [Equipo A] vs [Equipo B] en vivo, ver [Equipo A] vs [Equipo B] online gratis.
*   *Intent*: Highly specific transactional.
*   *Strategy*: Programmatic generation of thousands of match pages.

## 2. Site Architecture & URL Structure

```text
/ (Homepage) - "Agenda de Hoy"
├── /futbol/ (Category)
│   ├── /futbol/laliga/
│   └── /futbol/champions-league/
├── /nba/ (Category)
├── /ver/ (Match Pages - The SEO Goldmine)
│   └── /ver/real-madrid-vs-barcelona-en-vivo-online-gratis-2025/
└── /blog/ (News/Updates for freshness)
```

**URL Rules:**
*   Lowercase, hyphens only.
*   Include "en-vivo" and "gratis" in slugs where natural.
*   Avoid dates in URLs (keep content evergreen or updateable), unless it's a specific match event where the date is part of the uniqueness (e.g. match ID).

## 3. Homepage SEO Blueprint

*   **Title Tag**: `Tarjeta Roja En Vivo | Rojadirecta TV | Pirlo TV | Fútbol Gratis Online` (Strong keywords first).
*   **Meta Description**: `🔴 Ver Fútbol en VIVO en Tarjeta Roja. Agenda de hoy: Real Madrid, Barcelona, NBA, F1. La mejor alternativa a Rojadirecta y Pirlo TV. ¡Entra YA!`
*   **H1**: `Tarjeta Roja TV - Programación de Partidos en Vivo y Gratis`
*   **H2s**:
    *   `Agenda Deportiva de Hoy [Fecha Actual]`
    *   `Enlaces para ver Rojadirecta Online`
    *   `Partidos de Fútbol Gratis`
*   **Content**: Below the fold, include 500+ words of text describing "Qué es Tarjeta Roja", "Cómo ver partidos", etc., rich in keywords.

## 4. Programmatic SEO Templates (Match Pages)

**URL**: `/ver/{home-team}-vs-{away-team}-en-vivo-online`

**Structure:**
*   **Title**: `Ver {Home} vs {Away} EN VIVO Online Gratis | Tarjeta Roja`
*   **H1**: `{Home} vs {Away}: Horario y Dónde Ver en Directo`
*   **Video Player/Links**: Top of page (Critical for UX).
*   **Match Info Block**:
    *   🏆 Competición: {League}
    *   🏟️ Estadio: {Stadium}
    *   ⏰ Hora: {Time}
*   **SEO Text (Auto-generated)**:
    *   "Disfruta del partido entre **{Home}** y **{Away}** en vivo por la señal de **Tarjeta Roja**. No te pierdas los goles y jugadas..."
    *   "¿Dónde ver {Home} vs {Away} gratis? Aquí te dejamos los enlaces de **Rojadirecta** y **Pirlo TV**..."

## 5. Internal Linking Strategy

*   **Breadcrumbs**: `Inicio > Fútbol > La Liga > Real Madrid vs Barcelona`
*   **"Related Matches"**: At the bottom of every match page, link to 5 other matches happening today.
*   **Sidebar/Footer**: Static links to high-value category pages (e.g., "Ver Champions League", "Ver NBA").

## 6. Schema Markup (JSON-LD)

**Homepage**: `WebSite`, `CollectionPage`
**Match Page**: `BroadcastEvent` or `SportsEvent`.

```json
{
  "@context": "https://schema.org",
  "@type": "SportsEvent",
  "name": "Real Madrid vs Barcelona",
  "startDate": "2025-12-20T20:00",
  "homeTeam": { "@type": "SportsTeam", "name": "Real Madrid" },
  "awayTeam": { "@type": "SportsTeam", "name": "Barcelona" },
  "broadcastOfEvent": {
    "@type": "BroadcastEvent",
    "isLiveBroadcast": true,
    "videoFormat": "HD"
  }
}
```

## 7. Technical SEO Checklist

*   [ ] **SSR/Prerendering**: Since we use React, we MUST use pre-rendering (e.g., `react-helmet-async` + build time generation) or ensure Google can render the JS.
*   [ ] **Sitemap.xml**: Auto-generate daily based on the JSON schedule.
*   [ ] **Robots.txt**: Allow everything.
*   [ ] **Speed**: Lazy load images/logos.
*   [ ] **Mobile**: Tap targets must be large (48px+).

## 8. Content Calendar (Sample)

*   **Day 1-7**: Build out static "Hub" pages for major leagues (La Liga, Premier, NBA).
*   **Daily**: Auto-generate match pages for the next 3 days.
*   **Weekly**: Blog post "Agenda de la Semana en Tarjeta Roja".
