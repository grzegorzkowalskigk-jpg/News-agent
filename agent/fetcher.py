"""Moduł pobierania newsów z RSS."""

import feedparser
from dataclasses import dataclass
from datetime import datetime
from config import RSS_FEEDS, KEYWORDS, MAX_ARTICLES


@dataclass
class Article:
    title: str
    summary: str
    url: str
    source: str
    published: str


def fetch_articles() -> list[Article]:
    """Pobiera artykuły ze wszystkich skonfigurowanych feedów RSS."""
    articles = []

    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            source = feed.feed.get("title", feed_url)

            for entry in feed.entries:
                title = entry.get("title", "")
                summary = entry.get("summary", entry.get("description", ""))
                url = entry.get("link", "")
                published = entry.get("published", str(datetime.now()))

                # Filtrowanie po słowach kluczowych
                if KEYWORDS:
                    text = (title + " " + summary).lower()
                    if not any(kw.lower() in text for kw in KEYWORDS):
                        continue

                articles.append(Article(
                    title=title,
                    summary=summary,
                    url=url,
                    source=source,
                    published=published,
                ))

        except Exception as e:
            print(f"[fetcher] Błąd pobierania {feed_url}: {e}")

    return articles[:MAX_ARTICLES]
