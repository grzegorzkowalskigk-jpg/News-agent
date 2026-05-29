"""Punkt wejścia News Agent."""

from agent.fetcher import fetch_articles
from agent.summarizer import summarize_all
from agent.reporter import generate_report


def main():
    print("=== News Agent ===")

    print("\n[1/3] Pobieram artykuły z RSS...")
    articles = fetch_articles()
    print(f"      Pobrano {len(articles)} artykułów.")

    if not articles:
        print("Brak artykułów. Sprawdź konfigurację RSS_FEEDS w config.py.")
        return

    print("\n[2/3] Podsumowuję przez Claude...")
    summarized = summarize_all(articles)

    print("\n[3/3] Generuję raport...")
    report_path = generate_report(summarized)
    print(f"      Raport zapisany: {report_path}")

    print("\n=== Gotowe! ===")


if __name__ == "__main__":
    main()
