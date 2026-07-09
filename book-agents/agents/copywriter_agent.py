"""
Agente de Copywriting.
Toma la investigación de tendencias + los datos del libro y genera
contenido listo para publicar, en formato JSON estructurado por canal.
"""
import json
from .llm_client import ask_claude

SYSTEM_PROMPT = """Eres un copywriter experto en marketing editorial para ciencia ficción
y no-ficción especulativa. Escribes con la voz de marca que se te indique.
Responde ÚNICAMENTE con un objeto JSON válido, sin texto adicional, sin backticks,
con exactamente estas claves:
{
  "bluesky_post": "string, máximo 280 caracteres, con 1-2 hashtags",
  "mastodon_post": "string, máximo 480 caracteres",
  "reddit_title": "string, título neutral no-spam para r/scifi o similar",
  "reddit_body": "string, 3-5 frases, tono de recomendación genuina, no venta agresiva",
  "x_post_draft": "string, máximo 280 caracteres (para que el usuario lo publique manualmente)",
  "linkedin_post_draft": "string, 3-4 párrafos cortos, ángulo reflexivo/filosófico",
  "amazon_description_suggestion": "string, 2-3 párrafos optimizados para conversión, para que el usuario lo pegue en KDP/Author Central"
}"""


def run(book: dict, brand_voice: str, research_notes: str) -> dict:
    user_prompt = f"""
Voz de marca: {brand_voice}

Libro: {book['title']}
Pitch: {book.get('short_pitch', '')}
Temas: {', '.join(book.get('themes', []))}
Público objetivo: {book.get('target_audience', '')}
Link de Amazon: {book.get('amazon_url', '')}

Tendencias/investigación reciente para usar como gancho:
{research_notes}

Genera el contenido en el formato JSON exacto indicado.
"""
    raw = ask_claude(SYSTEM_PROMPT, user_prompt, max_tokens=1800)
    raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: guarda el texto crudo si el modelo no devolvió JSON limpio
        return {"raw_output": raw}
