"""Moduł generowania raportu z podsumowanych artykułów, pogrupowany po kategoriach."""

from datetime import datetime
from pathlib import Path
from config import CATEGORIES

# Ładne nagłówki kategorii w raporcie
_CATEGORY_LABELS = {
    "finanse": "💰 Finanse",
    "technologia": "💻 Technologia",
    "geopolityka": "🌍 Geopolityka",
    "zamowienia_rzadowe": "🏛️ Zamówienia rządowe",
}


def generate_report(articles: list[dict], output_dir: str = "reports") -> str:
    """Generuje raport Markdown pogrupowany po kategoriach i zwraca ścieżkę do pliku."""
    Path(output_dir).mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    path = f"{output_dir}/report_{timestamp}.md"

    lines = [
        f"# Raport newsów — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"Wybrano **{len(articles)}** istotnych artykułów.",
        "",
    ]

    # Grupowanie wg kolejności kategorii z config
    for cat_id in CATEGORIES:
        group = [a for a in articles if a.get("category") == cat_id]
        if not group:
            continue

        label = _CATEGORY_LABELS.get(cat_id, cat_id)
        lines += [f"## {label}", ""]

        for art in group:
            lines += [
                f"### {art['title']}  `({art['relevance']}/10)`",
                f"**Źródło:** {art['source']} | **Data:** {art['published']}",
                f"**Link:** {art['url']}",
                "",
                art["summary"],
                "",
            ]
        lines.append("---")
        lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return path
