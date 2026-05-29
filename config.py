import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Źródła RSS — wszystkie zweryfikowane jako żywe (HTTP 200). Pogrupowane po temacie.
RSS_FEEDS = [
    # 💰 Finanse
    "https://www.economist.com/finance-and-economics/rss.xml",   # The Economist – finanse
    "https://www.ft.com/rss/home",                              # Financial Times
    "https://www.bankier.pl/rss/wiadomosci.xml",                # Bankier (PL)
    "https://www.money.pl/rss/",                                # Money.pl (PL)
    # Reuters (własny RSS wycofany) – odzyskany przez Google News, filtr po domenie + temacie
    "https://news.google.com/rss/search?q=site:reuters.com+when:2d+business+OR+markets+OR+economy&hl=en-US&gl=US&ceid=US:en",

    # 💻 Technologia
    "https://techcrunch.com/feed/",                            # TechCrunch
    "https://feeds.arstechnica.com/arstechnica/index",         # Ars Technica
    "https://www.theverge.com/rss/index.xml",                  # The Verge
    "https://hnrss.org/frontpage",                             # Hacker News
    "https://news.google.com/rss/search?q=site:reuters.com+when:2d+technology+OR+tech&hl=en-US&gl=US&ceid=US:en",  # Reuters Tech

    # 🌍 Geopolityka
    "https://www.economist.com/international/rss.xml",          # The Economist – świat
    "https://foreignpolicy.com/feed/",                         # Foreign Policy
    "https://warontherocks.com/feed/",                         # War on the Rocks
    "https://www.defensenews.com/arc/outboundfeeds/rss/?outputType=xml",  # Defense News
    "https://news.google.com/rss/search?q=site:reuters.com+when:2d+world+OR+geopolitics+OR+politics&hl=en-US&gl=US&ceid=US:en",  # Reuters World

    # 🏛️ Zamówienia rządowe (US – kontrakty Pentagonu, codzienne, z nazwami spółek)
    "https://www.defense.gov/DesktopModules/ArticleCS/RSS.ashx?ContentType=9&Site=945&max=20",
    # TODO: TED (przetargi UE) – RSS wycofany, wymaga integracji Search API v3

    # ⚡ Szybkie / breaking
    "https://news.google.com/rss/search?q=site:apnews.com+when:1d&hl=en-US&gl=US&ceid=US:en",  # AP News (RSS wycofany)
    "https://trumpstruth.org/feed",                            # Posty Trumpa z Truth Social
]

# Maksymalna liczba artykułów pobieranych z JEDNEGO feedu (balans + kontrola kosztów)
MAX_PER_FEED = 15

# Konta X/Twitter pobierane przez most Nitter (wire-flashe market-moving).
# UWAGA: Nitter bywa niestabilny — instancję można podmienić, jeśli przestanie działać.
NITTER_INSTANCE = "https://nitter.net"
X_ACCOUNTS = [
    "FirstSquawk",      # breaking macro / market headlines
    "financialjuice",   # makro, FX, banki centralne
    "DeItaone",         # Walter Bloomberg – breaking market headlines
]

# Kategorie tematyczne — klucz = id, wartość = opis dla klasyfikatora
CATEGORIES = {
    "finanse": "rynki finansowe, gospodarka, banki centralne, akcje, waluty, inflacja, stopy procentowe",
    "technologia": "IT, AI, oprogramowanie, sprzęt, startupy, big tech, cyberbezpieczeństwo, internet",
    "geopolityka": "stosunki międzynarodowe, konflikty, wojny, dyplomacja, sankcje, sojusze, polityka zagraniczna",
    "zamowienia_rzadowe": "przetargi publiczne, kontrakty rządowe, zamówienia obronne, infrastruktura finansowana z budżetu",
}

# Minimalna istotność (0-10), poniżej której artykuł jest odrzucany
RELEVANCE_THRESHOLD = 5

# Maksymalna liczba artykułów POBIERANYCH łącznie ze wszystkich feedów (przed klasyfikacją).
# Z 13 feedów × MAX_PER_FEED=15 ≈ 195, więc limit dobrany tak, by każdy feed dołożył porcję.
MAX_FETCH = 200

# Maksymalna liczba artykułów PODSUMOWYWANYCH (po klasyfikacji, najistotniejsze)
MAX_SUMMARIZE = 15

# Świeżość: bierzemy tylko artykuły opublikowane w ciągu ostatnich N godzin.
# (None = bez filtra wieku). Interesują nas tylko najnowsze newsy.
MAX_AGE_HOURS = 24

# Cache przetworzonych URL-i — by nie klasyfikować tych samych artykułów w kółko.
CACHE_FILE = "seen_articles.json"
CACHE_PRUNE_DAYS = 7          # po ilu dniach zapominamy URL z cache

# Harmonogram: co ile minut odpalać agenta w trybie pętli (run_loop.py)
LOOP_INTERVAL_MIN = 20

# Modele Claude
CLASSIFIER_MODEL = "claude-haiku-4-6"   # tani filtr kategorii
CLAUDE_MODEL = "claude-sonnet-4-6"      # podsumowania
