# News Agent

AI agent do pobierania, czytania i podsumowywania wiadomości z różnych źródeł.

## Pipeline

```
RSS → klasyfikacja (Haiku) → filtr istotności → podsumowanie (Sonnet) → raport .md
```

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
│   ├── fetcher.py      # pobieranie newsów z RSS (+ deduplikacja)
│   ├── classifier.py   # klasyfikacja tematyczna + ocena istotności (Haiku)
│   ├── summarizer.py   # podsumowywanie zakwalifikowanych (Sonnet)
│   └── reporter.py     # raport Markdown pogrupowany po kategoriach
├── main.py             # punkt wejścia
├── config.py           # źródła RSS, kategorie, progi, modele
├── requirements.txt
└── README.md
```

## Planowane

- Wysyłka raportu na **Telegram** (Bot API — bez numeru telefonu)
- Harmonogram (cron / scheduled task)

## Uruchomienie

```bash
pip install -r requirements.txt
python main.py
```
