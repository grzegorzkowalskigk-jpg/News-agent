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
│   ├── fetcher.py      # pobieranie z RSS (round-robin, filtr świeżości, czyszczenie HTML)
│   ├── cache.py        # pamięć przetworzonych URL-i (bez powtórek)
│   ├── classifier.py   # klasyfikacja + market-impact + aktywa (Haiku)
│   ├── summarizer.py   # podsumowywanie zakwalifikowanych (Sonnet)
│   └── reporter.py     # raport Markdown pogrupowany po kategoriach
├── main.py             # pojedynczy przebieg
├── run_loop.py         # pętla co LOOP_INTERVAL_MIN minut
├── config.py           # źródła RSS, kategorie, progi, modele, harmonogram
├── requirements.txt
└── README.md
```

## Świeżość i cache

- **Filtr świeżości** (`MAX_AGE_HOURS`, domyślnie 24h) — bierzemy tylko najnowsze artykuły.
- **Cache** (`seen_articles.json`) — raz przetworzony URL nie trafia drugi raz do modelu.
  Przy każdym przebiegu klasyfikujemy więc tylko *nowe* artykuły. Wpisy starsze niż
  `CACHE_PRUNE_DAYS` są automatycznie usuwane.

## Uruchomienie

```bash
pip install -r requirements.txt
cp .env.example .env          # wpisz ANTHROPIC_API_KEY

python main.py                # pojedynczy przebieg
python run_loop.py            # pętla co LOOP_INTERVAL_MIN minut (Ctrl+C aby przerwać)
```

## Planowane

- Wysyłka raportu na **Telegram** (Bot API — bez numeru telefonu)
- TED (przetargi UE) przez Search API v3
- Szybsze źródła breaking-news (wire/Twitter) dla niższej latencji
