"""Moduł podsumowywania artykułów przez Claude API."""

import anthropic
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL
from agent.fetcher import Article


client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def summarize_article(article: Article) -> str:
    """Zwraca krótkie podsumowanie artykułu po polsku."""
    prompt = f"""Przeczytaj poniższy artykuł i napisz zwięzłe podsumowanie po polsku (2-3 zdania).

Tytuł: {article.title}
Źródło: {article.source}
Treść: {article.summary}

Podsumowanie:"""

    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()


def summarize_all(articles: list[Article]) -> list[dict]:
    """Podsumowuje listę artykułów i zwraca listę słowników."""
    results = []
    for i, article in enumerate(articles, 1):
        print(f"  [{i}/{len(articles)}] Podsumowuję: {article.title[:60]}...")
        summary = summarize_article(article)
        results.append({
            "title": article.title,
            "source": article.source,
            "url": article.url,
            "published": article.published,
            "summary": summary,
        })
    return results
