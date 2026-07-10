"""
Agente de SEO / Landing Page.
Reconstruye el README.md del repo como una "página de ventas" optimizada,
usando el contenido generado para todos los libros.
Esto es lo único que SÍ podemos publicar 100% automático en el propio repo
(GitHub Actions tiene permiso de escritura sobre su propio repositorio).
"""
from datetime import date


def build_readme(author_name: str, series_name: str, books_content: list, social_links: dict = None) -> str:
    social_links = social_links or {}
    lines = [
        f"# {series_name}",
        "",
        f"### por {author_name}",
        "",
        f"_Actualizado automáticamente por el equipo de agentes el {date.today().isoformat()}_",
        "",
        "---",
        "",
    ]

    for entry in books_content:
        book = entry["book"]
        content = entry["content"]
        lines.append(f"## {book['title']}")
        lines.append("")
        lines.append(f"**{book.get('short_pitch', '')}**")
        lines.append("")
        if isinstance(content, dict) and "amazon_description_suggestion" in content:
            lines.append(content["amazon_description_suggestion"])
        lines.append("")
        lines.append(f"👉 [Cómpralo en Amazon]({book.get('amazon_url', '#')})")
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append("### Sígueme")
    lines.append("")
    if social_links.get("x"):
        lines.append(f"- 𝕏 [X / Twitter]({social_links['x']})")
    if social_links.get("youtube"):
        lines.append(f"- ▶️ [YouTube]({social_links['youtube']})")
    if social_links.get("linkedin"):
        lines.append(f"- 💼 [LinkedIn]({social_links['linkedin']})")
    lines.append("- 🦋 [Bluesky](#) — actualizado automáticamente")
    lines.append("- 🐘 [Mastodon](#) — actualizado automáticamente")
    lines.append("")
    return "\n".join(lines)
