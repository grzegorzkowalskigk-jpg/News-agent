"""Pomocnik: wykrywa Twój chat_id do Telegrama.

Użycie:
1. Utwórz bota przez @BotFather, wklej token do .env (TELEGRAM_BOT_TOKEN).
2. Napisz do swojego bota dowolną wiadomość (np. "hej") na Telegramie.
3. Uruchom:  python scripts/get_chat_id.py
4. Skopiuj wypisany chat_id do .env (TELEGRAM_CHAT_ID).
"""

import sys
import os
import httpx

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TELEGRAM_BOT_TOKEN


def main():
    if not TELEGRAM_BOT_TOKEN:
        print("Brak TELEGRAM_BOT_TOKEN w .env — najpierw wklej token z @BotFather.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    data = httpx.get(url, timeout=20).json()

    if not data.get("ok"):
        print("Błąd API:", data)
        return

    updates = data.get("result", [])
    if not updates:
        print("Brak wiadomości. Napisz coś do bota na Telegramie i uruchom ponownie.")
        return

    seen = {}
    for u in updates:
        msg = u.get("message") or u.get("channel_post") or {}
        chat = msg.get("chat", {})
        if chat.get("id"):
            seen[chat["id"]] = chat.get("title") or chat.get("username") or chat.get("first_name", "")

    print("Znalezione czaty (wklej id do TELEGRAM_CHAT_ID w .env):")
    for cid, name in seen.items():
        print(f"  chat_id = {cid}   ({name})")


if __name__ == "__main__":
    main()
