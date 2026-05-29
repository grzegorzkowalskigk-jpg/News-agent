"""Pobieranie przetargów UE z oficjalnego TED API v3 (Tenders Electronic Daily).

TED wycofał RSS — zostało REST API (POST /v3/notices/search, bez klucza).
Filtrujemy po kodach CPV (obronność / IT), bo dziennie jest ~13 tys. ogłoszeń.
Pola wielojęzyczne (notice-title, buyer-name) to słowniki {lang: wartość}.
"""

import json
import urllib.request
import urllib.error
from datetime import datetime
from config import TED_CPV, TED_DAYS, TED_MAX
from agent.fetcher import Article

_API = "https://api.ted.europa.eu/v3/notices/search"
_HEADERS = {
    "User-Agent": "NewsAgent",
    "Content-Type": "application/json",
    "Accept": "application/json",
}
# Preferowana kolejność języków przy wyborze wartości z pola wielojęzycznego
_LANGS = ("eng", "ENG", "fra", "deu", "MUL")


def _pref(field) -> str:
    """Wyciąga tekst z pola TED, które bywa stringiem, listą lub słownikiem {lang: ...}."""
    if not field:
        return ""
    if isinstance(field, str):
        return field
    if isinstance(field, list):
        return _pref(field[0]) if field else ""
    if isinstance(field, dict):
        for lang in _LANGS:
            if lang in field:
                return _pref(field[lang])
        # fallback: pierwsza dostępna wartość
        return _pref(next(iter(field.values())))
    return str(field)


def _build_query() -> str:
    cpv = " OR ".join(f"classification-cpv={code}*" for code in TED_CPV)
    return f"({cpv}) AND publication-date>=today(-{TED_DAYS})"


def fetch_ted() -> list[Article]:
    """Zwraca listę ogłoszeń TED jako obiekty Article."""
    body = {
        "query": _build_query(),
        "fields": ["publication-number", "notice-title", "buyer-name",
                   "links", "contract-nature"],
        "page": 1,
        "limit": TED_MAX,
        "scope": "ALL",
    }
    req = urllib.request.Request(
        _API, data=json.dumps(body).encode(), headers=_HEADERS, method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode("utf-8", "ignore"))
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as e:
        print(f"[ted] Błąd pobierania TED API: {e}")
        return []

    out = []
    for n in data.get("notices", []):
        num = n.get("publication-number", "")
        title = _pref(n.get("notice-title")) or "(bez tytułu)"
        buyer = _pref(n.get("buyer-name"))
        nature = _pref(n.get("contract-nature"))

        # Link do strony ogłoszenia (html), w razie braku budujemy z numeru
        links = n.get("links") or {}
        url = _pref(links.get("html")) or _pref(links.get("htmlDirect"))
        if not url and num:
            url = f"https://ted.europa.eu/en/notice/{num}/html"

        summary = f"Przetarg UE (TED). Zamawiający: {buyer or 'b.d.'}. Typ: {nature or 'b.d.'}. {title}"

        out.append(Article(
            title=title,
            summary=summary,
            url=url,
            source="TED (przetargi UE)",
            published=str(datetime.now()),
        ))

    return out
