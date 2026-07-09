"""
Orquestador del equipo de agentes.
Flujo: Investigación -> Copywriting -> SEO/README -> Publicación.
Se ejecuta completo por GitHub Actions, sin intervención humana.
"""
import subprocess
import yaml

from agents import research_agent, copywriter_agent, seo_agent, youtube_agent
from publishers import bluesky_publish, mastodon_publish, reddit_publish, manual_drafts


def load_config(path: str = "config/books.yaml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def git_commit_and_push(paths: list, message: str):
    subprocess.run(["git", "config", "user.name", "book-marketing-bot"], check=True)
    subprocess.run(["git", "config", "user.email", "bot@users.noreply.github.com"], check=True)
    subprocess.run(["git", "add", *paths], check=True)
    result = subprocess.run(["git", "commit", "-m", message])
    if result.returncode == 0:
        subprocess.run(["git", "push"], check=True)
        print("[git] Cambios publicados en el repo.")
    else:
        print("[git] No hay cambios nuevos que commitear.")


def main():
    config = load_config()
    books = config["books"]
    brand_voice = config.get("brand_voice", "")

    all_entries = []

    for book in books:
        print(f"\n=== Procesando: {book['title']} ===")

        print("-> Agente de investigación...")
        research_notes = research_agent.run(book)

        print("-> Agente de copywriting...")
        content = copywriter_agent.run(book, brand_voice, research_notes)

        youtube_channel_id = config.get("youtube_channel_id", "")
        youtube_ideas = None
        if youtube_channel_id:
            print("-> Agente de YouTube (solo lectura + ideas)...")
            youtube_ideas = youtube_agent.run(book, youtube_channel_id)

        all_entries.append({"book": book, "content": content, "youtube_ideas": youtube_ideas})

        # Publicación real y automática (canales sin restricciones)
        if isinstance(content, dict):
            if content.get("bluesky_post"):
                bluesky_publish.publish(content["bluesky_post"])
            if content.get("mastodon_post"):
                mastodon_publish.publish(content["mastodon_post"])
            if content.get("reddit_title") and content.get("reddit_body"):
                # Cambia "scifi" por un subreddit que permita self-promo
                reddit_publish.publish("scifi", content["reddit_title"], content["reddit_body"])

    print("\n-> Agente de SEO / actualizando README...")
    readme = seo_agent.build_readme(
        config.get("author_name", ""),
        config.get("series_name", ""),
        all_entries,
        social_links=config.get("social_links", {}),
    )
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    print("-> Guardando borradores manuales (X, LinkedIn, Amazon)...")
    manual_drafts.save_drafts(all_entries)

    print("-> Commit y push de los cambios al repo...")
    git_commit_and_push(["README.md", "drafts/manual_review.md"], "🤖 Actualización automática de marketing")


if __name__ == "__main__":
    main()
