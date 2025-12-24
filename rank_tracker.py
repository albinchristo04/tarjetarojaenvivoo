import json
import os
import random
from datetime import datetime, timedelta

# Configuration
STATE_FILE = "seo_rank_state.json"
HISTORY_FILE = "seo_rank_history.json"

KEYWORDS = [
    "rojadirecta", "rojadirecta tv", "tarjeta roja", 
    "tarjeta roja en vivo", "tarjeta roja tv", "pirlotv", 
    "pirlo tv rojadirecta", "roja directa en vivo fútbol gratis", 
    "tarjeta roja fútbol en vivo"
]

def get_current_performance():
    """
    Agent 11: Performance Monitoring.
    In a production environment, this would call Google Search Console API.
    For this implementation, we simulate/placeholder the data fetch.
    """
    # Placeholder for GSC / SERP Scraping data
    performance = {}
    for kw in KEYWORDS:
        performance[kw] = {
            "position": random.uniform(1, 20),
            "impressions": random.randint(1000, 50000),
            "ctr": random.uniform(0.01, 0.15),
            "timestamp": datetime.now().isoformat()
        }
    return performance

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"pages": {}, "global_history": []}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def generate_optimized_elements(kw, reason):
    """Agent 11: Auto-Rewrite Logic."""
    modifiers = ["hoy", "gratis", "en vivo", "ahora", "directo", "HD"]
    emoji = random.choice(["⚽", "🔴", "📺", "🔥"])
    
    # Title formulas based on Agent 10 attack strategies
    titles = [
        f"{emoji} {kw.title()} | Ver Fútbol En Vivo {random.choice(modifiers)} ⚽",
        f"🔴 {kw.upper()} TV | Enlaces Gratis {random.choice(modifiers)} | Fútbol Hoy 📺",
        f"📺 {kw.title()} En Directo | {random.choice(modifiers)} Sin Cortes ⚽"
    ]
    
    new_title = random.choice(titles)[:60]
    new_h1 = f"Ver {kw.title()} en Vivo y Directo ({random.choice(modifiers)})"
    new_meta = f"🔴 Accede a {kw} en vivo. La mejor calidad para ver fútbol gratis {random.choice(modifiers)}. Enlaces actualizados cada hora. ¡Entra ya! ⚽"
    
    return {
        "title": new_title,
        "h1": new_h1,
        "meta": new_meta,
        "rewrite_date": datetime.now().isoformat(),
        "reason": reason
    }

def run_rank_tracker():
    print("📈 Agent 11: Running Rank Tracking & Auto-Rewrite Engine...")
    state = load_state()
    current_perf = get_current_performance()
    
    rewrites_triggered = []

    for kw, perf in current_perf.items():
        page_key = kw.replace(" ", "-")
        if page_key not in state["pages"]:
            state["pages"][page_key] = {"history": [], "current_elements": None, "last_rewrite": None}
        
        history = state["pages"][page_key]["history"]
        history.append(perf)
        # Keep last 30 days
        state["pages"][page_key]["history"] = history[-30:]
        
        # Trigger Logic
        trigger = False
        reason = ""
        
        if len(history) >= 2:
            prev_pos = history[-2]["position"]
            curr_pos = perf["position"]
            
            # 1. Drop >= 3 positions
            if curr_pos - prev_pos >= 3:
                trigger = True
                reason = "Drop >= 3 positions"
            
            # 2. Flat >= 7 days (simplified check)
            elif len(history) >= 7 and all(abs(h["position"] - curr_pos) < 0.5 for h in history[-7:]):
                trigger = True
                reason = "Stagnation (Flat 7 days)"
                
            # 3. High impressions + Low CTR
            elif perf["impressions"] > 10000 and perf["ctr"] < 0.02:
                trigger = True
                reason = "Low CTR on high impressions"

        # Check 7-day cooldown
        last_rewrite = state["pages"][page_key].get("last_rewrite")
        if last_rewrite:
            last_date = datetime.fromisoformat(last_rewrite)
            if datetime.now() - last_date < timedelta(days=7):
                trigger = False

        if trigger:
            print(f"⚠️ Triggering rewrite for '{kw}' due to {reason}")
            new_elements = generate_optimized_elements(kw, reason)
            
            # A/B Safety: Store old for rollback
            state["pages"][page_key]["previous_elements"] = state["pages"][page_key].get("current_elements")
            state["pages"][page_key]["current_elements"] = new_elements
            state["pages"][page_key]["last_rewrite"] = datetime.now().isoformat()
            rewrites_triggered.append({"kw": kw, "reason": reason, "new": new_elements})

    save_state(state)
    print(f"✅ Rank Tracking Complete. {len(rewrites_triggered)} rewrites applied.")
    return state

if __name__ == "__main__":
    run_rank_tracker()
