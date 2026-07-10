"""
X (Twitter), LinkedIn personal y la ficha de Amazon (KDP) NO tienen forma
de publicarse 100% automática sin cuentas de desarrollador de pago o revisión
de app. En vez de fingir automatización, guardamos los borradores en un
archivo Markdown dentro del repo para que los copies y pegues en 30 segundos.
"""
from datetime import date


def save_drafts(entries: list, path: str = "drafts/manual_review.md"):
    lines = [f"# Borradores para publicar manualmente — {date.today().isoformat()}", ""]
    for entry in entries:
        book = entry["book"]
        content = entry["content"]
        lines.append(f"## {book['title']}")
        lines.append("")
        if isinstance(content, dict):
            if "x_post_draft" in content:
                lines.append("**X (Twitter):**")
                lines.append(f"> {content['x_post_draft']}")
                lines.append("")
            if "linkedin_post_draft" in content:
                lines.append("**LinkedIn:**")
                lines.append(content["linkedin_post_draft"])
                lines.append("")
            if "amazon_description_suggestion" in content:
                lines.append("**Sugerencia de descripción para Amazon/KDP:**")
                lines.append(content["amazon_description_suggestion"])
                lines.append("")
        if entry.get("youtube_ideas"):
            lines.append("**Ideas de video/short para YouTube:**")
            lines.append(entry["youtube_ideas"])
            lines.append("")
        lines.append("---")
        lines.append("")

    import os
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[manual_drafts] Guardado en {path}")
