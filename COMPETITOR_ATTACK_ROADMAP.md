# 🕵️ AGENT 10 — COMPETITOR REVERSE-ENGINEERING & ATTACK ROADMAP

## 1. Competitor Weakness Matrix

| Competitor Type | Main Weakness | Attack Strategy |
| :--- | :--- | :--- |
| **Rojadirecta Clones** | Thin content, high ad density, broken links. | Deploy 1000+ word match pages with verified player links. |
| **Pirlo TV Mirrors** | Poor mobile optimization, slow LCP. | Use static HTML (Vite/Python) for <1s load times. |
| **Aggregators** | Generic titles, lack of Schema. | Use "Emotional H1s" + SportsEvent & FAQ Schema. |
| **Legacy Sites** | Infrequent updates (daily). | Hourly rebuilds via GitHub Actions + IndexNow pings. |

## 2. Structural Advantages to Exploit
- **Static Depth:** While competitors rely on PHP/Database calls, our site is 100% static HTML, making it 10x faster and easier for Googlebot to crawl.
- **Schema Saturation:** Most competitors ignore Schema. We implement `SportsEvent`, `FAQPage`, and `BroadcastEvent` on every single match page.
- **Internal Authority Loop:** Our Hub pages (`/rojadirecta/`) funnel authority directly to the latest match pages, creating a "freshness boost" that competitors lack.

## 3. Title Rewrite Formulas (CTR Attack)
*Beat competitors by using these high-CTR patterns:*
- **Pattern A:** `🔴 Ver [Event] EN VIVO Online Gratis Hoy | Tarjeta Roja TV ⚽`
- **Pattern B:** `📺 [Event] EN DIRECTO Gratis | Rojadirecta TV | Enlaces [Time] 🔴`
- **Pattern C:** `⚽ [Event] Online Gratis | Pirlo TV vs Tarjeta Roja | Ver YA 🔴`

## 4. Priority Attack Roadmap
1. **High ROI:** Optimize Match Page Titles & Schema (COMPLETED).
2. **High ROI:** Deploy Parasite SEO Authority Buffers (AGENT 9).
3. **Medium ROI:** Expand Hub Page content to 1500+ words (IN PROGRESS).
4. **Medium ROI:** Implement "Related Matches" sidebar for internal link depth.

## 5. Elements to Copy/Improve/Discard
- **Copy:** Use of "Canal 1, Canal 2" naming convention (users trust it).
- **Improve:** The "Shield" logic. Competitors use annoying popups; we use a single-click shield that blocks ads.
- **Discard:** Sidebar widgets that slow down mobile rendering.
