import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Źródła RSS do monitorowania
RSS_FEEDS = [
    "https://feeds.bbci.co.uk/news/rss.xml",            # BBC News
    "https://rss.cnn.com/rss/edition.rss",              # CNN
    "https://feeds.reuters.com/reuters/topNews",        # Reuters
    "https://www.investing.com/rss/news.rss",           # Investing.com
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

# Maksymalna liczba artykułów POBIERANYCH z RSS (przed klasyfikacją)
MAX_FETCH = 60

# Maksymalna liczba artykułów PODSUMOWYWANYCH (po klasyfikacji, najistotniejsze)
MAX_SUMMARIZE = 15

# Modele Claude
CLASSIFIER_MODEL = "claude-haiku-4-6"   # tani filtr kategorii
CLAUDE_MODEL = "claude-sonnet-4-6"      # podsumowania
