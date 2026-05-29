"""Moduł klasyfikacji tematycznej artykułów przez tani model Claude (Haiku).

Każdy artykuł dostaje kategorię (jedną z config.CATEGORIES albo None) oraz
ocenę istotności 0-10. Artykuły bez kategorii lub poniżej progu są odrzucane.
"""

import json
import anthropic
from config import (
    ANTHROPIC_API_KEY,
    CLASSIFIER_MODEL,
    CATEGORIES,
    RELEVANCE_THRESHOLD,
)
from agent.fetcher import Article


client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

_VALID = set(CATEGORIES.keys())

_CATEGORY_BLOCK = "\n".join(f'- "{key}": {desc}' for key, desc in CATEGORIES.items())

_SYSTEM = f"""Jesteś klasyfikatorem wiadomości. Przypisujesz artykuł do JEDNEJ z kategorii:
{_CATEGORY_BLOCK}

Jeśli artykuł nie pasuje do żadnej kategorii, użyj "brak".
Oceń też istotność (relevance) w skali 0-10: jak ważny/wartościowy jest artykuł
w obrębie swojej kategorii (10 = przełomowy, 0 = trywialny/clickbait).

Odpowiadasz WYŁĄCZNIE poprawnym JSON-em, bez komentarzy:
{{"category": "<id_kategorii_lub_brak>", "relevance": <0-10>}}"""


def _classify_one(article: Article) -> tuple[str | None, int]:
    """Zwraca (kategoria|None, istotność)."""
    user = f"Tytuł: {article.title}\nLead: {article.summary[:500]}"

    try:
        msg = client.messages.create(
            model=CLASSIFIER_MODEL,
            max_tokens=60,
            system=_SYSTEM,
            messages=[{"role": "user", "content": user}],
        )
        raw = msg.content[0].text.strip()
        data = json.loads(raw)
        category = data.get("category", "brak")
        relevance = int(data.get("relevance", 0))

        if category not in _VALID:
            return None, relevance
        return category, relevance

    except (json.JSONDecodeError, ValueError, KeyError, IndexError) as e:
        print(f"[classifier] Nie sparsowano odpowiedzi dla '{article.title[:50]}': {e}")
        return None, 0
    except Exception as e:
        print(f"[classifier] Błąd API dla '{article.title[:50]}': {e}")
        return None, 0


def classify_and_filter(articles: list[Article]) -> list[Article]:
    """Klasyfikuje artykuły i zwraca tylko te z kategorią i istotnością >= próg,
    posortowane malejąco po istotności."""
    kept = []
    for i, art in enumerate(articles, 1):
        category, relevance = _classify_one(art)
        art.category = category
        art.relevance = relevance

        status = "✗ odrzucony"
        if category and relevance >= RELEVANCE_THRESHOLD:
            kept.append(art)
            status = f"✓ {category} ({relevance})"
        print(f"  [{i}/{len(articles)}] {status}: {art.title[:55]}")

    kept.sort(key=lambda a: a.relevance, reverse=True)
    return kept
