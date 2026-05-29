"""Cache przetworzonych artykułów — pamięta URL-e, które już sklasyfikowaliśmy,
żeby przy kolejnych uruchomieniach nie przepuszczać ich ponownie przez model.

Format pliku: {"<url>": "<iso_timestamp>", ...}
Wpisy starsze niż CACHE_PRUNE_DAYS są usuwane przy każdym zapisie.
"""

import json
import os
from datetime import datetime, timedelta
from config import CACHE_FILE, CACHE_PRUNE_DAYS
from agent.fetcher import Article


def _load() -> dict:
    if not os.path.exists(CACHE_FILE):
        return {}
    try:
        with open(CACHE_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _save(data: dict) -> None:
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _parse(ts: str) -> datetime:
    try:
        return datetime.fromisoformat(ts)
    except (ValueError, TypeError):
        return datetime.min


def filter_new(articles: list[Article]) -> list[Article]:
    """Zwraca tylko artykuły, których URL nie ma jeszcze w cache."""
    seen = _load()
    return [a for a in articles if a.url not in seen]


def mark_seen(articles: list[Article]) -> None:
    """Zapamiętuje URL-e jako przetworzone i czyści stare wpisy."""
    seen = _load()
    now = datetime.now()
    for a in articles:
        seen[a.url] = now.isoformat()

    # Pruning — wyrzucamy wpisy starsze niż CACHE_PRUNE_DAYS
    cutoff = now - timedelta(days=CACHE_PRUNE_DAYS)
    seen = {u: t for u, t in seen.items() if _parse(t) > cutoff}

    _save(seen)
