"""
Publica automáticamente en un subreddit usando PRAW.
⚠️ ÚSALO CON CUIDADO: Reddit banea cuentas que publican auto-promoción
sin participar en la comunidad. Recomendado: usar solo en subreddits que
permitan explícitamente self-promo, y no más de 1 vez por semana por sub.
Requiere Secrets: REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME,
REDDIT_PASSWORD (créalos gratis en https://www.reddit.com/prefs/apps).
"""
import os
import praw


def publish(subreddit_name: str, title: str, body: str) -> bool:
    required = ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USERNAME", "REDDIT_PASSWORD"]
    if not all(os.environ.get(v) for v in required):
        print("[reddit] Secrets no configurados, se omite publicación.")
        return False
    try:
        reddit = praw.Reddit(
            client_id=os.environ["REDDIT_CLIENT_ID"],
            client_secret=os.environ["REDDIT_CLIENT_SECRET"],
            username=os.environ["REDDIT_USERNAME"],
            password=os.environ["REDDIT_PASSWORD"],
            user_agent="post-singularity-books-bot/1.0",
        )
        subreddit = reddit.subreddit(subreddit_name)
        subreddit.submit(title=title, selftext=body)
        print(f"[reddit] Publicado en r/{subreddit_name}.")
        return True
    except Exception as e:
        print(f"[reddit] Error al publicar: {e}")
        return False
