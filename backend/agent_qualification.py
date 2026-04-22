import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configuration Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro')
else:
    model = None
    print("ATTENTION: GEMINI_API_KEY non définie. L'agent ne pourra pas fonctionner.")

def qualify_lead(lead_data: str) -> str:
    """
    Analyse les données d'un lead (transcription, formulaire, messages) et le score sur 100.
    Utilise la méthode BANT (Budget, Authority, Need, Timing).
    """
    if not model:
        return '{"error": "GEMINI_API_KEY manquante"}'

    prompt = f"""
    En tant qu'Agent de Qualification Commerciale IA (Business Partner IA), tu dois analyser 
    les informations suivantes concernant un prospect et lui attribuer un score de qualification sur 100.
    
    Critères à évaluer (BANT) :
    - Budget : Ont-ils les moyens de s'offrir nos services (Agence Marketing Digital) ?
    - Autorité : Sont-ils décideurs ?
    - Besoin (Need) : Leur problème correspond-il à notre offre (création site web, photo/vidéo, Ads) ?
    - Temporalité (Timing) : Est-ce un projet urgent ou lointain ?

    Données du prospect :
    {lead_data}

    Réponds OBLIGATOIREMENT ET UNIQUEMENT avec ce format JSON strict :
    {{
        "score": 85,
        "justification": "Explication détaillée du score basé sur BANT.",
        "next_action": "Appeler immédiatement | Nurturing | Rejeter"
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f'{{"error": "{str(e)}"}}'

if __name__ == "__main__":
    # Script de test local
    print("--- Test de l'Agent de Qualification ---")
    test_lead = "Bonjour, je suis le CEO d'une startup e-commerce. Nous faisons 50k€ de MRR, et nous cherchons une agence pour scaler nos publicités Meta Ads car nous visons une levée de fonds dans 3 mois. Notre budget d'agence est de 3000€/mois."
    
    print("\n[Données Lead] :", test_lead)
    print("\n[Analyse Gemini] :")
    resultat = qualify_lead(test_lead)
    print(resultat)
