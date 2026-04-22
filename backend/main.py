from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import json

import database
import agent_qualification

app = FastAPI(title="Business Partner IA API", version="1.0.0")

@app.on_event("startup")
def on_startup():
    # Initialisation de la base de données au démarrage de l'API
    database.init_db()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

class LeadRequest(BaseModel):
    name: str
    contact_info: str
    source: str
    raw_data: str

@app.get("/")
def read_root():
    return {"status": "online", "service": "Business Partner IA - Cerveau Backend"}

@app.post("/api/v1/agents/qualify-lead")
def qualify_new_lead(lead_req: LeadRequest, db: Session = Depends(get_db)):
    """
    Endpoint appelé par n8n lorsqu'un nouveau lead arrive (via formulaire, WhatsApp, etc.).
    Fait appel à l'Agent Gemini pour scorer le lead, et sauvegarde le résultat en base de données.
    """
    # Appel de l'agent IA
    ia_response_str = agent_qualification.qualify_lead(lead_req.raw_data)
    
    score = None
    justification = None
    next_action = None
    
    try:
        ia_data = json.loads(ia_response_str)
        score = ia_data.get("score")
        justification = ia_data.get("justification")
        next_action = ia_data.get("next_action")
    except json.JSONDecodeError:
        justification = "Erreur de parsing de la réponse IA : " + ia_response_str
    
    # Enregistrement en base de données
    new_lead = database.Lead(
        name=lead_req.name,
        contact_info=lead_req.contact_info,
        source=lead_req.source,
        raw_data=lead_req.raw_data,
        ai_score=score,
        ai_justification=justification,
        ai_next_action=next_action
    )
    
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    
    return {
        "status": "success",
        "lead_id": new_lead.id,
        "ai_analysis": {
            "score": score,
            "justification": justification,
            "next_action": next_action
        }
    }
