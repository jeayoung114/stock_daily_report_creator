# Daily Stock Report Generation App

## Overview
This application generates a comprehensive daily stock report based on user input. It leverages real-time data, news, and financial indicators to assist users in making informed buy/sell/hold decisions. The final report is exported as a Word document.

---

## Features

1. **User Input**
   - User enters the stock name or ticker symbol.

2. **Data Gathering**
   - Fetches recent news articles and social media comments related to the stock.
   - Retrieves recent stock prices and generates a price chart.
   - Collects key financial indicators (e.g., PER, PBR, EPS, market cap, etc.).

3. **Report Generation**
   - Summarizes findings in bullet points.
   - Provides a detailed narrative report.
   - Offers a buy/sell/hold suggestion based on the data.

4. **Export**
   - Exports the generated report as a Word (.docx) document.

---

## Agent-Based MCP Architecture

This app uses an agent-based Multi-step, Chain-of-Thought, or Multi-Agent Collaboration Pattern (MCP) powered by the OpenAI API. Each agent is responsible for a specific part of the workflow, coordinated by an Orchestrator agent.

### Agents and Responsibilities

- **Orchestrator Agent:**
  - Manages the workflow, delegates tasks, and compiles results.
- **Data Collection Agent:**
  - Gathers stock data, news, social sentiment, and financial indicators from APIs.
- **Analysis Agent:**
  - Summarizes news/comments and analyzes data using OpenAI API (summarization, sentiment analysis).
- **Report Generation Agent:**
  - Creates bullet points, detailed narrative, and buy/sell/hold suggestion using OpenAI API.
- **Export Agent:**
  - Formats and exports the report as a Word document.

### Workflow Example

1. **User Input:**
   - User provides stock name/ticker.
2. **Orchestrator Agent:**
   - Receives input, triggers Data Collection Agent.
3. **Data Collection Agent:**
   - Crawls APIs for news, social sentiment, stock prices, and financials.
   - Returns raw data to Orchestrator.
4. **Analysis Agent:**
   - Summarizes news and comments (using OpenAI API for summarization/sentiment).
   - Analyzes financials and price trends.
   - Returns insights to Orchestrator.
5. **Report Generation Agent:**
   - Generates bullet points and detailed report (using OpenAI API for text generation).
   - Suggests buy/sell/hold (rule-based or LLM-based).
   - Returns report to Orchestrator.
6. **Export Agent:**
   - Formats the report and exports as a Word document.

### OpenAI API Usage

- **Summarization:** Use GPT-4 for summarizing news and comments.
- **Sentiment Analysis:** Use GPT-4 or a fine-tuned model for sentiment.
- **Report Generation:** Use GPT-4 for bullet points, detailed narrative, and suggestions.

### Example MCP Flow (Pseudocode)

```python
# Orchestrator Agent
def generate_stock_report(stock_name):
    data = data_collection_agent(stock_name)
    insights = analysis_agent(data)
    report = report_generation_agent(insights)
    export_agent(report, filename=f"{stock_name}_report.docx")
```

### Benefits of Agent-Based MCP

- **Modularity:** Each agent can be improved or replaced independently.
- **Scalability:** Easy to add more agents (e.g., for new data sources).
- **Transparency:** Each step is traceable and debuggable.

---

## Technical Considerations

- **Programming Language:** Python (recommended for data, NLP, and docx support)
- **APIs/Libraries:**
  - News: newsapi, Google News, etc.
  - Social: Tweepy (Twitter), PRAW (Reddit)
  - Stock Data: yfinance, Alpha Vantage
  - Charting: matplotlib, plotly
  - Word Export: python-docx
- **NLP:** Summarization and sentiment analysis (spaCy, NLTK, transformers, OpenAI API)
- **UI:** CLI for MVP, web UI (Flask/Streamlit) for future
- **Scheduling:** Optionally, automate daily report generation

---

## MVP Scope
- CLI app
- Input: Stock name/ticker
- Output: Word doc report with news, comments, price chart, indicators, and suggestion
- Agent-based MCP using OpenAI API for analysis and report generation

---

## Future Enhancements
- Web-based UI
- User authentication and history
- More advanced ML-based recommendation
- Multi-stock batch reports
- Email or cloud export options

---

## Workflow Visualization

Below is the current workflow graph for the agent-based stock report system:

![LangGraph Workflow](output/langgraph_workflow.pdf)