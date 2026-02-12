# agents/llm_client.py

import os
from dotenv import load_dotenv
from google import genai  

from utils.json_cleaner import clean_and_parse_json

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY environment variable is not set.")

client = genai.Client(api_key=API_KEY)


def call_llm_json(prompt: str, model: str = "gemini-3-flash-preview"):
    """
    Appelle le modèle Gemini pour générer du contenu JSON strict.
    Retourne un objet Python déjà parsé (list/dict).
    """
    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                response_mime_type="application/json"
            ),
        )

        raw_text = response.text or ""
        return clean_and_parse_json(raw_text)
    except Exception as e:
        raise Exception(f"Erreur LLM: {e}")


def call_llm(prompt: str) -> str:
    """
    Compatibilité rétro : renvoie toujours une chaîne JSON nettoyée.
    Utilisé par l'agent FSD existant.
    """
    obj = call_llm_json(prompt)
    import json

    return json.dumps(obj, ensure_ascii=False, indent=2)
