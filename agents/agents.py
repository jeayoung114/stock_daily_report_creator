# agents/agents.py
"""
Defines the main agent classes for the stock report app.
"""
import datetime
from agents.news_fetcher import NewsFetcher
import openai
import os

class NewsAgent:
    def __init__(self):
        self.fetcher = NewsFetcher()

    def collect(self, stock_name: str):
        news = self.fetcher.fetch_news(stock_name)
        return {"news": news}

class PriceAgent:
    def collect(self, stock_name: str):
        import yfinance as yf
        ticker = yf.Ticker(stock_name)
        hist = ticker.history(period="5d")
        prices = [
            {"date": str(idx.date()), "close": float(row["Close"])}
            for idx, row in hist.iterrows()
        ]
        return {"prices": prices}

class FinancialsAgent:
    def collect(self, stock_name: str):
        import yfinance as yf
        ticker = yf.Ticker(stock_name)
        info = ticker.info
        financials = {
            "PER": info.get("trailingPE"),
            "PBR": info.get("priceToBook"),
            "EPS": info.get("trailingEps"),
            "market_cap": info.get("marketCap"),
        }
        return {"financials": financials}

class SocialSentimentAgent:
    def collect(self, stock_name: str):
        # Example: Use newsapi to fetch social sentiment from news headlines as a proxy
        # For real implementation, integrate with Twitter, Reddit, or StockTwits APIs
        from newsapi import NewsApiClient
        import os
        api_key = os.getenv("NEWSAPI_KEY")
        if not api_key:
            # Fallback to mock if no API key
            print("[SocialSentimentAgent] No API key found. Returning mock comments.")
            comments = [
                {"user": "investor123", "text": f"I think {stock_name} will go up!", "sentiment": "positive"},
                {"user": "skeptic456", "text": f"Not sure about {stock_name} at these prices.", "sentiment": "neutral"},
            ]
            return {"comments": comments}
        client = NewsApiClient(api_key=api_key)
        articles = client.get_everything(q=stock_name, language='en', sort_by='publishedAt', page_size=5)
        comments = []
        for a in articles.get("articles", []):
            comments.append({
                "user": a.get("source", {}).get("name", "news"),
                "text": a.get("title", ""),
                "sentiment": "unknown"  # Sentiment analysis can be added later
            })
        return {"comments": comments}

class MarketIndicesAgent:
    def collect(self):
        import yfinance as yf
        indices = {}
        for symbol, name in [("^GSPC", "S&P500"), ("^IXIC", "NASDAQ")]:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            if not data.empty:
                indices[name] = float(data["Close"].iloc[-1])
            else:
                indices[name] = None
        return {"indices": indices}

class DataCollectionAgent:
    def __init__(self):
        self.news_agent = NewsAgent()
        self.price_agent = PriceAgent()
        self.financials_agent = FinancialsAgent()
        self.social_agent = SocialSentimentAgent()
        self.indices_agent = MarketIndicesAgent()

    def collect(self, stock_name: str):
        print(f"[DataCollectionAgent] Collecting data for {stock_name}")
        try:
            news = self.news_agent.collect(stock_name)["news"]
            prices = self.price_agent.collect(stock_name)["prices"]
            financials = self.financials_agent.collect(stock_name)["financials"]
            comments = self.social_agent.collect(stock_name)["comments"]
            indices = self.indices_agent.collect()["indices"]
            return {
                "stock_name": stock_name,
                "prices": prices,
                "news": news,
                "comments": comments,
                "financials": financials,
                "indices": indices,
            }
        except Exception as e:
            print(f"[DataCollectionAgent] Error fetching real data: {e}. Using mock data.")
            return self.get_mock_data(stock_name)

    def get_mock_data(self, stock_name: str):
        today = datetime.date.today().isoformat()
        return {
            "stock_name": stock_name,
            "prices": [
                {"date": today, "close": 150.25},
                {"date": "2024-06-06", "close": 148.90},
                {"date": "2024-06-05", "close": 147.50},
            ],
            "news": [
                {"title": f"{stock_name} hits new high", "summary": "The stock reached a new high today amid strong earnings.", "date": today, "url": ""},
                {"title": f"Analysts bullish on {stock_name}", "summary": "Several analysts upgraded their outlook.", "date": today, "url": ""},
            ],
            "comments": [
                {"user": "investor123", "text": f"I think {stock_name} will go up!", "sentiment": "positive"},
                {"user": "skeptic456", "text": f"Not sure about {stock_name} at these prices.", "sentiment": "neutral"},
            ],
            "financials": {
                "PER": 18.5,
                "PBR": 2.1,
                "EPS": 8.25,
                "market_cap": "120B USD",
            },
            "indices": {
                "S&P500": 5300.12,
                "NASDAQ": 17000.45,
            }
        }

class AnalysisAgent:
    def analyze(self, data):
        print("[AnalysisAgent] Analyzing data")
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            print("[AnalysisAgent] No OpenAI API key found. Returning basic summaries.")
            return self.basic_analyze(data)
        openai.api_key = openai_api_key
        # Summarize news
        news_text = "\n".join([f"- {item['title']}: {item['summary']}" for item in data.get("news", [])])
        news_summary = self.summarize_with_openai(news_text, "Summarize the following news headlines and summaries about the stock:")
        # Summarize comments
        comments_text = "\n".join([f"- {item['text']}" for item in data.get("comments", [])])
        comments_summary = self.summarize_with_openai(comments_text, "Summarize the following social comments about the stock:")
        # Summarize price trend
        prices = data.get("prices", [])
        price_trend = self.summarize_price_trend(prices)
        # Summarize financials
        financials = data.get("financials", {})
        financials_summary = self.summarize_financials(financials)
        return {
            "news_summary": news_summary,
            "comments_summary": comments_summary,
            "price_trend": price_trend,
            "financials_summary": financials_summary,
        }

    def summarize_with_openai(self, text, prompt):
        if not text.strip():
            return "No data available."
        # Use GPT-4.0 or GPT-4.1 model
        response = openai.resources.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[{"role": "system", "content": prompt}, {"role": "user", "content": text}],
            max_tokens=128
        )
        return response.choices[0].message.content.strip()

    def summarize_price_trend(self, prices):
        if not prices:
            return "No price data available."
        closes = [p["close"] for p in prices]
        if len(closes) < 2:
            return "Not enough price data."
        trend = closes[-1] - closes[0]
        direction = "upward" if trend > 0 else ("downward" if trend < 0 else "flat")
        return f"The price trend over the period is {direction} ({closes[0]:.2f} → {closes[-1]:.2f})."

    def summarize_financials(self, financials):
        if not financials:
            return "No financial data available."
        return (
            f"PER: {financials.get('PER', 'N/A')}, "
            f"PBR: {financials.get('PBR', 'N/A')}, "
            f"EPS: {financials.get('EPS', 'N/A')}, "
            f"Market Cap: {financials.get('market_cap', 'N/A')}"
        )

    def basic_analyze(self, data):
        # Fallback if no OpenAI API key
        news_titles = [item['title'] for item in data.get('news', [])]
        comments = [item['text'] for item in data.get('comments', [])]
        prices = data.get('prices', [])
        financials = data.get('financials', {})
        return {
            "news_summary": f"News: {', '.join(news_titles)}",
            "comments_summary": f"Comments: {', '.join(comments)}",
            "price_trend": self.summarize_price_trend(prices),
            "financials_summary": self.summarize_financials(financials),
        }

class ReportGenerationAgent:
    def generate(self, insights):
        print("[ReportGenerationAgent] Generating report")
        return {}

class ExportAgent:
    def export(self, report, filename: str):
        print(f"[ExportAgent] Exporting report to {filename}")