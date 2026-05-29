"""Moduł pobierania newsów z RSS."""

import re
import html
import time
import calendar
import feedparser
from dataclasses import dataclass, field
from datetime import datetime
from config import (
    RSS_FEEDS, MAX_FETCH, MAX_PER_FEED, MAX_AGE_HOURS,
    NITTER_INSTANCES, X_ACCOUNTS, TED_ENABLED,
)

_TAG_RE = re.compile(r"<[^>]+>")


def _clean(text: str) -> str:
    """Usuwa tagi HTML i dekoduje encje — leady z RSS bywają zaśmiecone."""
    text = _TAG_RE.sub(" ", text or "")
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


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
    market_impact: int = 0
    assets: list[str] = field(default_factory=list)


def _parse_feed(feed_url: str, source_override: str | None = None) -> list[Article]:
    """Pobiera i normalizuje do MAX_PER_FEED artykułów z jednego feedu.

    source_override — wymusza nazwę źródła (np. "X / @FirstSquawk" dla Nittera)."""
    out = []
    try:
        feed = feedparser.parse(feed_url)
        feed_title = feed.feed.get("title", feed_url)

        for entry in feed.entries[:MAX_PER_FEED]:
            url = entry.get("link", "")
            if not url:
                continue

            # Filtr świeżości — pomijamy artykuły starsze niż MAX_AGE_HOURS
            pub = entry.get("published_parsed") or entry.get("updated_parsed")
            if MAX_AGE_HOURS and pub:
                age_h = (time.time() - calendar.timegm(pub)) / 3600
                if age_h > MAX_AGE_HOURS:
                    continue

            # Źródło: override (Nitter) → z wpisu (Google News → "Reuters") → z feedu
            if source_override:
                source = source_override
            else:
                src = entry.get("source", {})
                source = src.get("title") if isinstance(src, dict) and src.get("title") else feed_title

            title = _clean(entry.get("title", ""))
            # Google News dokleja " - Źródło" na końcu tytułu — usuń
            if source and title.endswith(f" - {source}"):
                title = title[: -len(f" - {source}")].strip()
            summary = _clean(entry.get("summary", entry.get("description", "")))
            # Google News daje w summary tylko link → fallback na tytuł
            if len(summary) < 30:
                summary = title

            out.append(Article(
                title=title,
                summary=summary,
                url=url,
                source=source,
                published=entry.get("published", str(datetime.now())),
            ))
    except Exception as e:
        print(f"[fetcher] Błąd pobierania {feed_url}: {e}")
    return out


def _fetch_x(account: str) -> list[Article]:
    """Pobiera tweety konta przez Nitter, próbując kolejnych instancji aż któraś
    zwróci wpisy (Nitter rate-limituje/pada losowo)."""
    for instance in NITTER_INSTANCES:
        articles = _parse_feed(f"{instance}/{account}/rss", source_override=f"X / @{account}")
        if articles:
            return articles
    print(f"[fetcher] X/@{account}: żadna instancja Nittera nie zwróciła wpisów")
    return []


def fetch_articles() -> list[Article]:
    """Pobiera artykuły ze wszystkich feedów i przeplata je round-robin,
    żeby globalny limit MAX_FETCH nie zagłodził feedów z końca listy."""
    per_feed = [_parse_feed(u) for u in RSS_FEEDS]
    # Konta X/Twitter przez Nitter — z fallbackiem między instancjami
    for acct in X_ACCOUNTS:
        per_feed.append(_fetch_x(acct))
    # TED — przetargi UE przez API (lazy import: ted_fetcher importuje Article stąd)
    if TED_ENABLED:
        from agent.ted_fetcher import fetch_ted
        per_feed.append(fetch_ted())

    articles = []
    seen_urls = set()
    i = 0
    # Przeplatanie: po jednym artykule z każdego feedu, aż wyczerpiemy wszystkie
    while len(articles) < MAX_FETCH and any(i < len(f) for f in per_feed):
        for feed_articles in per_feed:
            if i < len(feed_articles):
                art = feed_articles[i]
                if art.url in seen_urls:
                    continue
                seen_urls.add(art.url)
                articles.append(art)
                if len(articles) >= MAX_FETCH:
                    break
        i += 1

    return articles
