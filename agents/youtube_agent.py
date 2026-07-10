"""
Agente de YouTube — modo lectura + generación de ideas.

Usa la YouTube Data API v3 con una simple API KEY (gratis, cuota diaria
gratuita de Google) para leer tus videos recientes. Con esa info + los
libros, le pide a Claude que genere ideas/guiones de video o shorts.

IMPORTANTE: esto NO publica nada en YouTube. Publicar (community posts,
subir video, editar descripción) requiere OAuth2 con tu autorización
explícita como dueño del canal — una API key sola no tiene permiso de
escritura por diseño de Google. Si más adelante quieres publicar de verdad,
se necesita un flujo OAuth aparte (client_id + client_secret + refresh_token).
"""
import os
import requests
from .llm_client import ask_claude

YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3"

SYSTEM_PROMPT = """Eres un guionista de contenido para YouTube especializado en
ciencia ficción especulativa, IA y transhumanismo. Con la lista de videos
recientes del canal y los datos del libro, genera 3 ideas de video/short
concretas (título + gancho de 2 líneas + estructura de 3-4 puntos) que
conecten el catálogo de videos existente con el libro a promocionar.
No inventes datos de los videos que no te di. Sé breve y accionable."""


def get_recent_videos(channel_id: str, max_results: int = 5) -> list:
    """Lee los videos más recientes del canal (solo lectura, gratis)."""
    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key or not channel_id:
        print("[youtube] Falta YOUTUBE_API_KEY o channel_id, se omite.")
        return []
    try:
        search_resp = requests.get(
            f"{YOUTUBE_API_URL}/search",
            params={
                "key": api_key,
                "channelId": channel_id,
                "part": "snippet",
                "order": "date",
                "maxResults": max_results,
                "type": "video",
            },
            timeout=15,
        )
        search_resp.raise_for_status()
        items = search_resp.json().get("items", [])
        return [
            {
                "title": item["snippet"]["title"],
                "published_at": item["snippet"]["publishedAt"],
            }
            for item in items
        ]
    except Exception as e:
        print(f"[youtube] Error leyendo el canal: {e}")
        return []


def run(book: dict, channel_id: str) -> str:
    recent_videos = get_recent_videos(channel_id)
    videos_text = (
        "\n".join(f"- {v['title']} ({v['published_at'][:10]})" for v in recent_videos)
        or "(no se pudieron leer videos recientes)"
    )
    user_prompt = f"""
Libro: {book['title']}
Pitch: {book.get('short_pitch', '')}
Temas: {', '.join(book.get('themes', []))}

Videos recientes del canal:
{videos_text}

Genera 3 ideas de video/short conectando el canal con este libro.
"""
    return ask_claude(SYSTEM_PROMPT, user_prompt, max_tokens=900)
