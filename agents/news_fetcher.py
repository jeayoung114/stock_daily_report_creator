# agents/news_fetcher.py
"""
Modular NewsFetcher for fetching news headlines using NewsAPI.
"""
import os
from newsapi import NewsApiClient
import datetime

class NewsFetcher:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("NEWSAPI_KEY")
        if self.api_key:
            self.client = NewsApiClient(api_key=self.api_key)
        else:
            self.client = None

    def fetch_news(self, query, max_articles=5):
        today = datetime.date.today().isoformat()
        if not self.client:
            print("[NewsFetcher] No API key found. Returning mock news.")
            return self.mock_news(query, today)
        try:
            articles = self.client.get_everything(q=query, language='en', sort_by='publishedAt', page_size=max_articles)
            news = [
                {
                    "title": a["title"],
                    "summary": a["description"] or "",
                    "date": a["publishedAt"][:10],
                    "url": a["url"]
                }
                for a in articles.get("articles", [])
            ]
            return news
        except Exception as e:
            print(f"[NewsFetcher] Error fetching news: {e}. Returning mock news.")
            return self.mock_news(query, today)

    def mock_news(self, query, today):
        return [
            {"title": f"{query} hits new high", "summary": "The stock reached a new high today amid strong earnings.", "date": today, "url": ""},
            {"title": f"Analysts bullish on {query}", "summary": "Several analysts upgraded their outlook.", "date": today, "url": ""},
        ] 