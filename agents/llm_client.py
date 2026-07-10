"""
Cliente mínimo para llamar a la API de Gemini (Google) desde cualquier agente.
Requiere la variable de entorno GEMINI_API_KEY (se configura como Secret en GitHub).

Mantiene la misma firma que el cliente de Claude (ask_claude) para que los
agentes no tengan que cambiar su lógica interna, solo el import.
"""
import os
import requests

MODEL = "gemini-2.5-flash"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def ask_claude(system_prompt: str, user_prompt: str, use_web_search: bool = False, max_tokens: int = 2000) -> str:
    """Llama a Gemini con un prompt de sistema (rol del agente) y uno de usuario (tarea)."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Falta GEMINI_API_KEY. Configúrala como Secret en tu repo de GitHub "
            "(Settings > Secrets and variables > Actions)."
        )

    payload = {
        "system_instruction": {"parts": [{"text": system_prompt}]},
        "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
        "generationConfig": {"maxOutputTokens": max_tokens},
    }
    if use_web_search:
        # Grounding con Google Search, equivalente a la herramienta web_search de Claude
        payload["tools"] = [{"google_search": {}}]

    url = API_URL.format(model=MODEL)
    response = requests.post(url, params={"key": api_key}, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()

    try:
        parts = data["candidates"][0]["content"]["parts"]
        return "\n".join(p.get("text", "") for p in parts).strip()
    except (KeyError, IndexError):
        raise RuntimeError(f"Respuesta inesperada de Gemini: {data}")
