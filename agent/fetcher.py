"""Moduł pobierania newsów z RSS."""

import feedparser
from dataclasses import dataclass
from datetime import datetime
from config import RSS_FEEDS, MAX_FETCH


@dataclass
class Article:
    title: str
    summary: str
    url: str
    source: str
    published: str
    # Wypełniane przez classifier.py
    category: str | None = None
    relevance: int = 0


def fetch_articles() -> list[Article]:
    """Pobiera artykuły ze wszystkich skonfigurowanych feedów RSS."""
    articles = []
    seen_urls = set()

    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            source = feed.feed.get("title", feed_url)

            for entry in feed.entries:
                url = entry.get("link", "")
                if url in seen_urls:        # deduplikacja
                    continue
                seen_urls.add(url)

                articles.append(Article(
                    title=entry.get("title", ""),
                    summary=entry.get("summary", entry.get("description", "")),
                    url=url,
                    source=source,
                    published=entry.get("published", str(datetime.now())),
                ))

        except Exception as e:
            print(f"[fetcher] Błąd pobierania {feed_url}: {e}")

    return articles[:MAX_FETCH]
