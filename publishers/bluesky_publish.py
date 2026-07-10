"""
Publica automáticamente en Bluesky usando la librería atproto.
Requiere los Secrets: BLUESKY_HANDLE y BLUESKY_APP_PASSWORD
(la app password se genera en Bluesky > Settings > App Passwords, es gratis).
"""
import os
from atproto import Client


def publish(text: str) -> bool:
    handle = os.environ.get("BLUESKY_HANDLE")
    app_password = os.environ.get("BLUESKY_APP_PASSWORD")
    if not handle or not app_password:
        print("[bluesky] Secrets no configurados, se omite publicación.")
        return False
    try:
        client = Client()
        client.login(handle, app_password)
        client.send_post(text=text[:300])
        print("[bluesky] Publicado correctamente.")
        return True
    except Exception as e:
        print(f"[bluesky] Error al publicar: {e}")
        return False
