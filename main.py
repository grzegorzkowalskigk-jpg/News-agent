"""Punkt wejścia News Agent."""

from agent.fetcher import fetch_articles
from agent.classifier import classify_and_filter
from agent.summarizer import summarize_all
from agent.reporter import generate_report
from config import MAX_SUMMARIZE


def main():
    print("=== News Agent ===")

    print("\n[1/4] Pobieram artykuły z RSS...")
    articles = fetch_articles()
    print(f"      Pobrano {len(articles)} artykułów.")
    if not articles:
        print("Brak artykułów. Sprawdź RSS_FEEDS w config.py.")
        return

    print("\n[2/4] Klasyfikuję tematycznie (Haiku)...")
    relevant = classify_and_filter(articles)
    print(f"      Zakwalifikowano {len(relevant)} artykułów.")
    if not relevant:
        print("Żaden artykuł nie pasuje do kategorii powyżej progu istotności.")
        return

    # Bierzemy najistotniejsze (lista jest już posortowana malejąco)
    relevant = relevant[:MAX_SUMMARIZE]

    print(f"\n[3/4] Podsumowuję {len(relevant)} artykułów (Sonnet)...")
    summarized = summarize_all(relevant)

    print("\n[4/4] Generuję raport...")
    report_path = generate_report(summarized)
    print(f"      Raport zapisany: {report_path}")

    print("\n=== Gotowe! ===")


if __name__ == "__main__":
    main()
