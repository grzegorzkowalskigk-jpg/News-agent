"""Wysyłka newsów na Telegram przez Bot API.

Każdy zakwalifikowany artykuł leci jako osobna "karta" (styl breaking-news).
Konfiguracja: TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID w .env.
"""

import html
import time
import httpx
from config import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    TELEGRAM_MIN_IMPACT,
)
from agent.reporter import _CATEGORY_LABELS

_API = "https://api.telegram.org/bot{token}/sendMessage"
_MAX_LEN = 4096          # limit długości wiadomości Telegrama


def telegram_ready() -> bool:
    """Czy Telegram jest skonfigurowany (token + chat_id)."""
    return bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)


def _impact_dot(impact: int) -> str:
    if impact >= 8:
        return "🔴"
    if impact >= 6:
        return "🟠"
    return "🟡"


def _format(article: dict) -> str:
    """Buduje treść wiadomości w HTML (Telegram parse_mode=HTML)."""
    esc = html.escape
    impact = article.get("market_impact", 0)
    cat = _CATEGORY_LABELS.get(article.get("category"), article.get("category") or "")
    assets = article.get("assets") or []

    lines = [
        f"{_impact_dot(impact)} <b>{esc(article['title'])}</b>",
        f"📈 Impact {impact}/10 · {cat}",
    ]
    if assets:
        lines.append(f"🎯 {esc(', '.join(assets))}")
    lines.append("")
    lines.append(esc(article["summary"]))
    lines.append("")
    lines.append(f"<i>{esc(article['source'])}</i> · <a href=\"{esc(article['url'])}\">źródło</a>")

    text = "\n".join(lines)
    return text[:_MAX_LEN]


def _send(text: str) -> bool:
    url = _API.format(token=TELEGRAM_BOT_TOKEN)
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    try:
        r = httpx.post(url, json=payload, timeout=20)
        if r.status_code != 200:
            print(f"[telegram] Błąd {r.status_code}: {r.text[:200]}")
            return False
        return True
    except httpx.HTTPError as e:
        print(f"[telegram] Wyjątek HTTP: {e}")
        return False


def send_to_telegram(articles: list[dict]) -> int:
    """Wysyła zakwalifikowane artykuły (powyżej progu impact). Zwraca liczbę wysłanych."""
    if not telegram_ready():
        print("[telegram] Pominięto — brak TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID w .env.")
        return 0

    sent = 0
    for art in articles:
        if art.get("market_impact", 0) < TELEGRAM_MIN_IMPACT:
            continue
        if _send(_format(art)):
            sent += 1
            time.sleep(0.5)     # delikatny throttling pod limity Telegrama
    print(f"[telegram] Wysłano {sent} wiadomości.")
    return sent
