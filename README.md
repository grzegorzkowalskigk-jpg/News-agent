# News Agent

AI agent do pobierania, czytania i podsumowywania wiadomości z różnych źródeł.

## Pipeline

```
RSS (13 źródeł) → klasyfikacja + ocena market-impact (Haiku) → filtr istotności
              → sortowanie po potencjale rynkowym → podsumowanie (Sonnet) → raport .md
```

Cel agenta: wyłapywać informacje i przecieki mogące **poruszyć cenami aktywów**.
Klasyfikator dla każdego artykułu zwraca kategorię, istotność (0-10),
**market_impact (0-10)** oraz listę powiązanych aktywów (spółki / tickery / instrumenty).
Selekcja idzie wg potencjału rynkowego.

## Źródła (PL + EN, bez tłumaczenia)

- **Finanse:** The Economist, Financial Times, Bankier, Money.pl
- **Technologia:** TechCrunch, Ars Technica, The Verge, Hacker News
- **Geopolityka:** The Economist (International), Foreign Policy, War on the Rocks, Defense News
- **Zamówienia rządowe:** US DoD Contracts (kontrakty Pentagonu)
  - ⏳ TED (przetargi UE) — RSS wycofany, wymaga integracji Search API v3 (TODO)
- **⚡ Szybkie / breaking:**
  - AP News (przez Google News — własny RSS wycofany)
  - Trump's Truth Social (trumpstruth.org)
  - Konta X/Twitter przez most **Nitter** — lista w `X_ACCOUNTS` (config.py).
    Domyślnie: @DeItaone, @FirstSquawk, @financialjuice.
    ⚠️ Nitter bywa niestabilny (rate-limituje konta losowo); instancję
    podmienisz w `NITTER_INSTANCE`.

> Uwaga o latencji: RSS + pętla co 20 min nie dorówna sub-minutowym flashom
> z terminala Bloomberga. Konta X (Nitter) i Trump Truth to najszybsze, co
> daje się złapać darmowo; niżej zejdziesz tylko płatnym API X / wire'ów.

## Kategorie tematyczne

- 💰 **Finanse** — rynki, gospodarka, banki centralne, waluty
- 💻 **Technologia** — AI, IT, big tech, cyberbezpieczeństwo
- 🌍 **Geopolityka** — konflikty, dyplomacja, sankcje, sojusze
- 🏛️ **Zamówienia rządowe** — przetargi publiczne, kontrakty obronne

Artykuły nieprzypisane do żadnej kategorii lub poniżej progu istotności
(`RELEVANCE_THRESHOLD`) są odrzucane.

## Struktura

```
News-agent/
├── agent/
│   ├── fetcher.py      # pobieranie z RSS (round-robin, filtr świeżości, Nitter fallback)
│   ├── ted_fetcher.py  # przetargi UE z TED API v3 (filtr CPV)
│   ├── cache.py        # pamięć przetworzonych URL-i (bez powtórek)
│   ├── classifier.py   # klasyfikacja + market-impact + aktywa (Haiku)
│   ├── summarizer.py   # podsumowywanie zakwalifikowanych (Sonnet)
│   ├── reporter.py     # raport Markdown pogrupowany po kategoriach
│   └── notifier.py     # wysyłka kart na Telegram (Bot API)
├── scripts/
│   └── get_chat_id.py  # pomocnik do wykrycia chat_id Telegrama
├── main.py             # pojedynczy przebieg
├── run_loop.py         # pętla co LOOP_INTERVAL_MIN minut
├── config.py           # źródła, kategorie, progi, modele, harmonogram, Telegram
├── requirements.txt
└── README.md
```

## Świeżość i cache

- **Filtr świeżości** (`MAX_AGE_HOURS`, domyślnie 24h) — bierzemy tylko najnowsze artykuły.
- **Cache** (`seen_articles.json`) — raz przetworzony URL nie trafia drugi raz do modelu.
  Przy każdym przebiegu klasyfikujemy więc tylko *nowe* artykuły. Wpisy starsze niż
  `CACHE_PRUNE_DAYS` są automatycznie usuwane.

## Telegram

Agent wysyła każdy zakwalifikowany news jako osobną „kartę" na Telegram
(impact, kategoria, powiązane aktywa, link). Konfiguracja bez numeru telefonu:

1. Utwórz bota przez **@BotFather** → skopiuj token do `.env` (`TELEGRAM_BOT_TOKEN`).
2. Napisz do swojego bota dowolną wiadomość na Telegramie.
3. `python scripts/get_chat_id.py` → skopiuj `chat_id` do `.env` (`TELEGRAM_CHAT_ID`).
4. Gotowe — kolejny przebieg `main.py` wyśle newsy na Telegram.

Próg wysyłki: `TELEGRAM_MIN_IMPACT` (0 = wszystkie zakwalifikowane; np. 7 = tylko
najmocniejsze sygnały). Wyłączenie: `TELEGRAM_ENABLED = False`.

## Uruchomienie

```bash
pip install -r requirements.txt
cp .env.example .env          # wpisz ANTHROPIC_API_KEY (+ Telegram, opcjonalnie)

python main.py                # pojedynczy przebieg
python run_loop.py            # pętla co LOOP_INTERVAL_MIN minut (Ctrl+C aby przerwać)
```

## Planowane

- Szybsze źródła breaking-news (płatne API X / wire'y) dla niższej latencji
- Przyciski akcji w wiadomościach Telegram (archiwizuj / więcej)
