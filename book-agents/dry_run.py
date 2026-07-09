"""
DRY RUN — simula el equipo de agentes con respuestas falsas (sin llamar a la
API real de Anthropic ni a ninguna red social) para validar que la lógica de
orquestación, el formato del README y los borradores funcionan bien.

Esto NO reemplaza la prueba real en GitHub Actions con tus Secrets — es solo
para depurar el código de forma segura y gratuita antes de eso.
"""
import sys
import yaml

sys.path.insert(0, ".")
from agents import seo_agent
from publishers import manual_drafts


def fake_research(book):
    return (
        f"- Avances recientes en modelos de lenguaje a gran escala conectan con "
        f"el tema de '{book['themes'][0]}' en {book['title']}.\n"
        f"- Debate público sobre consciencia artificial, relevante para el pitch del libro."
    )


def fake_copywriter(book, brand_voice, research_notes):
    return {
        "bluesky_post": f"¿Qué pasa cuando las mentes se fusionan? {book['title']} explora justo eso. #scifi",
        "mastodon_post": f"Nuevo post sobre {book['title']}: una mirada a la mente post-humana en la era de la IA.",
        "reddit_title": f"Recomendación: {book['title']} — ciencia ficción sobre mentes digitales",
        "reddit_body": f"Llevo tiempo pensando en cómo la IA cambiará la identidad humana, y {book['title']} lo aborda de forma que me hizo repensar varias cosas. Lo recomiendo si te gusta el hard sci-fi filosófico.",
        "x_post_draft": f"{book['title']}: ¿la próxima frontera de la mente humana? {book.get('amazon_url','')}",
        "linkedin_post_draft": f"He estado reflexionando sobre el futuro de la cognición humana.\n\n{book['title']} es mi intento de explorar esas preguntas en forma de ficción.\n\n¿Qué pasa cuando el pensamiento deja de ser individual?",
        "amazon_description_suggestion": f"{book['title']} es un viaje especulativo hacia un futuro donde la inteligencia ya no está confinada a una sola mente. Ideal para lectores de ciencia ficción dura y filosofía de la tecnología.",
    }


def fake_youtube_ideas(book):
    return (
        f"1. 'Cómo escribí {book['title']}' — detrás de escena, 3 puntos: inspiración, investigación, tema central.\n"
        f"2. 'Explicando {book['themes'][0]} en 60 segundos' — short conectando el tema con la trama.\n"
        f"3. Reacción a noticias recientes de IA relacionándolas con el libro."
    )


def main():
    with open("config/books.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    all_entries = []
    for book in config["books"]:
        print(f"\n=== [DRY RUN] Procesando: {book['title']} ===")
        research_notes = fake_research(book)
        content = fake_copywriter(book, config.get("brand_voice", ""), research_notes)
        youtube_ideas = fake_youtube_ideas(book)
        all_entries.append({"book": book, "content": content, "youtube_ideas": youtube_ideas})
        print("Contenido generado (simulado):")
        for k, v in content.items():
            print(f"  {k}: {v[:80]}...")

    readme = seo_agent.build_readme(
        config.get("author_name", ""),
        config.get("series_name", ""),
        all_entries,
        social_links=config.get("social_links", {}),
    )
    with open("README.dryrun.md", "w", encoding="utf-8") as f:
        f.write(readme)

    manual_drafts.save_drafts(all_entries, path="drafts/manual_review.dryrun.md")

    print("\n✅ Dry run completo. Revisa README.dryrun.md y drafts/manual_review.dryrun.md")


if __name__ == "__main__":
    main()
