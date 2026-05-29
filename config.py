import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Źródła RSS do monitorowania
RSS_FEEDS = [
    "https://feeds.bbci.co.uk/news/rss.xml",           # BBC News
    "https://rss.cnn.com/rss/edition.rss",              # CNN
    "https://feeds.reuters.com/reuters/topNews",         # Reuters
    "https://www.investing.com/rss/news.rss",           # Investing.com
]

# Filtrowanie — słowa kluczowe (puste = pobierz wszystko)
KEYWORDS = []

# Liczba artykułów do podsumowania na jedno uruchomienie
MAX_ARTICLES = 10

# Model Claude
CLAUDE_MODEL = "claude-sonnet-4-6"
