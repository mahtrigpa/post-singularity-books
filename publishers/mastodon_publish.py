"""
Publica automáticamente en Mastodon usando Mastodon.py.
Requiere los Secrets: MASTODON_API_BASE_URL (ej: https://mastodon.social)
y MASTODON_ACCESS_TOKEN (se genera gratis en tu instancia > Preferencias >
Desarrollo > Nueva aplicación, con permiso 'write:statuses').
"""
import os
from mastodon import Mastodon


def publish(text: str) -> bool:
    base_url = os.environ.get("MASTODON_API_BASE_URL")
    token = os.environ.get("MASTODON_ACCESS_TOKEN")
    if not base_url or not token:
        print("[mastodon] Secrets no configurados, se omite publicación.")
        return False
    try:
        mastodon = Mastodon(access_token=token, api_base_url=base_url)
        mastodon.status_post(text[:480])
        print("[mastodon] Publicado correctamente.")
        return True
    except Exception as e:
        print(f"[mastodon] Error al publicar: {e}")
        return False
