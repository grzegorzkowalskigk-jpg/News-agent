"""Klasyfikacja tematyczna + ocena potencjału rynkowego (Haiku).

Dla każdego artykułu model zwraca:
- category       : jedna z config.CATEGORIES albo "brak"
- relevance      : 0-10, jak istotny jest artykuł w obrębie kategorii
- market_impact  : 0-10, potencjał wywołania ruchu cen aktywów na giełdzie
- assets         : lista spółek / tickerów / instrumentów, których news dotyczy

Filtr: zostają artykuły z poprawną kategorią i relevance >= próg.
Sortowanie: malejąco po market_impact (cel = sygnały rynkowe), potem relevance.
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

_SYSTEM = f"""Jesteś analitykiem wiadomości pod kątem rynków finansowych.

Przypisz artykuł do JEDNEJ kategorii:
{_CATEGORY_BLOCK}
Jeśli nie pasuje do żadnej, użyj "brak".

Oceń dwie skale 0-10:
- relevance: jak ważny jest artykuł w obrębie swojej kategorii.
- market_impact: jak duży potencjał ma do wywołania ruchu cen aktywów na giełdzie
  (akcje, indeksy, surowce, waluty, krypto). Przecieki, kontrakty, decyzje
  regulacyjne, wyniki, fuzje = wysoki impact; komentarze ogólne = niski.

Wypisz "assets": konkretne spółki, tickery lub instrumenty, których news dotyczy
(np. ["Lockheed Martin", "LMT"], ["EUR/USD"], ["ropa Brent"]). Jeśli brak
konkretnego aktywa, podaj pustą listę [].

Odpowiadasz WYŁĄCZNIE poprawnym JSON-em, bez komentarzy:
{{"category": "<id_lub_brak>", "relevance": <0-10>, "market_impact": <0-10>, "assets": ["..."]}}"""


def _classify_one(article: Article) -> dict:
    """Zwraca dict z polami category/relevance/market_impact/assets."""
    user = f"Tytuł: {article.title}\nLead: {article.summary[:500]}"
    fallback = {"category": None, "relevance": 0, "market_impact": 0, "assets": []}

    try:
        msg = client.messages.create(
            model=CLASSIFIER_MODEL,
            max_tokens=200,
            system=_SYSTEM,
            messages=[{"role": "user", "content": user}],
        )
        data = json.loads(msg.content[0].text.strip())

        category = data.get("category", "brak")
        if category not in _VALID:
            category = None

        assets = data.get("assets", [])
        if not isinstance(assets, list):
            assets = []

        return {
            "category": category,
            "relevance": int(data.get("relevance", 0)),
            "market_impact": int(data.get("market_impact", 0)),
            "assets": [str(a) for a in assets],
        }

    except (json.JSONDecodeError, ValueError, KeyError, IndexError) as e:
        print(f"[classifier] Nie sparsowano '{article.title[:50]}': {e}")
        return fallback
    except Exception as e:
        print(f"[classifier] Błąd API '{article.title[:50]}': {e}")
        return fallback


def classify_and_filter(articles: list[Article]) -> list[Article]:
    """Klasyfikuje, odfiltrowuje poniżej progu i sortuje po potencjale rynkowym."""
    kept = []
    for i, art in enumerate(articles, 1):
        res = _classify_one(art)
        art.category = res["category"]
        art.relevance = res["relevance"]
        art.market_impact = res["market_impact"]
        art.assets = res["assets"]

        if art.category and art.relevance >= RELEVANCE_THRESHOLD:
            kept.append(art)
            tag = f"✓ {art.category} rel={art.relevance} impact={art.market_impact}"
            if art.assets:
                tag += f" → {', '.join(art.assets[:3])}"
        else:
            tag = "✗ odrzucony"
        print(f"  [{i}/{len(articles)}] {tag}: {art.title[:55]}")

    # Sortuj wg potencjału rynkowego (cel agenta), potem ogólnej istotności
    kept.sort(key=lambda a: (a.market_impact, a.relevance), reverse=True)
    return kept
