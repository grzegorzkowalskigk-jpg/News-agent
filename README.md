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
