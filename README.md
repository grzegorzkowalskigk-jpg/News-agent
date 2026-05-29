# News Agent

AI agent do pobierania, czytania i podsumowywania wiadomości z różnych źródeł.

## Funkcje (planowane)

- Pobieranie wiadomości z RSS / API (np. NewsAPI, GNews)
- Filtrowanie po tematach / słowach kluczowych
- Podsumowywanie artykułów przez Claude API
- Eksport do raportu (Markdown / Word)

## Struktura

```
News-agent/
├── agent/
│   ├── fetcher.py      # pobieranie newsów
│   ├── summarizer.py   # podsumowywanie przez Claude
│   └── reporter.py     # generowanie raportu
├── main.py             # punkt wejścia
├── config.py           # konfiguracja (klucze API, źródła)
├── requirements.txt
└── README.md
```

## Uruchomienie

```bash
pip install -r requirements.txt
python main.py
```
