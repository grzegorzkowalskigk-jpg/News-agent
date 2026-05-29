"""Moduł generowania raportu z podsumowanych artykułów."""

from datetime import datetime
from pathlib import Path


def generate_report(articles: list[dict], output_dir: str = "reports") -> str:
    """Generuje raport Markdown i zwraca ścieżkę do pliku."""
    Path(output_dir).mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    path = f"{output_dir}/report_{timestamp}.md"

    lines = [
        f"# Raport newsów — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"Pobrano **{len(articles)}** artykułów.",
        "",
        "---",
        "",
    ]

    for i, article in enumerate(articles, 1):
        lines += [
            f"## {i}. {article['title']}",
            f"**Źródło:** {article['source']} | **Data:** {article['published']}",
            f"**Link:** {article['url']}",
            "",
            article["summary"],
            "",
            "---",
            "",
        ]

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return path
