import json
import os
import re
from datetime import datetime

# Configuration
PAA_DATA_FILE = "paa_questions.json"
SEED_KEYWORDS = [
    "rojadirecta", "rojadirecta tv", "tarjeta roja", 
    "tarjeta roja en vivo", "tarjeta roja tv", "pirlotv", 
    "pirlo tv rojadirecta", "roja directa en vivo fútbol gratis", 
    "tarjeta roja fútbol en vivo"
]

def normalize_question(q):
    """Normalize and deduplicate questions."""
    q = q.lower().strip()
    q = re.sub(r'[¿?¡!]', '', q)
    return q

def classify_intent(q):
    """Classify intent and map to page types."""
    q = q.lower()
    if any(word in q for word in ["hoy", "ahora", "mañana", "fecha"]):
        return "freshness", "date"
    if any(word in q for word in ["donde", "cómo", "ver", "gratis", "en vivo"]):
        return "transactional", "match"
    if any(word in q for word in ["qué es", "quién", "oficial", "seguro"]):
        return "informational", "hub"
    return "navigational", "hub"

def prioritize_question(q, frequency):
    """Prioritize based on frequency and relevance."""
    score = frequency * 10
    if "gratis" in q.lower() or "en vivo" in q.lower():
        score += 20
    
    if score > 50:
        return "tier-1", score
    if score > 20:
        return "tier-2", score
    return "tier-3", score

def run_paa_intelligence():
    print("🤖 Agent 13: Running PAA Intelligence Engine...")
    
    # In a real scenario, this would be populated by a scraper or API
    # Seeding with real data found during browser session
    raw_questions = [
        "¿Dónde puedo ver fútbol gratis?",
        "¿Cómo ver DAZN gratis sin pagar?",
        "¿Cómo ver UEFA TV gratis?",
        "¿Dónde ver el Real Madrid hoy?",
        "¿Qué es Tarjeta Roja En Vivo?",
        "¿Es seguro ver fútbol en Tarjeta Roja?",
        "¿Cómo funciona Rojadirecta TV?",
        "¿Cuál es la página oficial de Rojadirecta?",
        "¿Cómo ver Pirlo TV online gratis?",
        "¿Qué partidos transmite Pirlo TV hoy?"
    ]
    
    # Load existing data
    if os.path.exists(PAA_DATA_FILE):
        with open(PAA_DATA_FILE, 'r', encoding='utf-8') as f:
            paa_db = json.load(f)
    else:
        paa_db = {}

    processed_count = 0
    for q in raw_questions:
        norm_q = normalize_question(q)
        if norm_q not in paa_db:
            intent, page_type = classify_intent(q)
            tier, score = prioritize_question(q, 1) # Initial frequency 1
            
            paa_db[norm_q] = {
                "original": q,
                "intent": intent,
                "target_page_type": page_type,
                "priority": tier,
                "score": score,
                "timestamp": datetime.now().isoformat()
            }
            processed_count += 1
        else:
            # Increment frequency/score if already exists
            paa_db[norm_q]["score"] += 5
            tier, _ = prioritize_question(paa_db[norm_q]["original"], paa_db[norm_q]["score"] / 10)
            paa_db[norm_q]["priority"] = tier

    # Save updated database
    with open(PAA_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(paa_db, f, indent=2, ensure_ascii=False)
        
    print(f"✅ PAA Intelligence Complete. Processed {processed_count} new questions.")
    return paa_db

if __name__ == "__main__":
    run_paa_intelligence()
