from langgraph import Workflow, Node
from agents.agents import NewsAgent, PriceAgent, FinancialsAgent, SocialSentimentAgent, MarketIndicesAgent, AnalysisAgent, ReportGenerationAgent, ExportAgent

def news_collection_node(inputs):
    agent = NewsAgent()
    news = agent.collect(inputs["stock_name"])["news"]
    return {"news": news}

def price_collection_node(inputs):
    agent = PriceAgent()
    prices = agent.collect(inputs["stock_name"])["prices"]
    return {"prices": prices}

def financials_collection_node(inputs):
    agent = FinancialsAgent()
    financials = agent.collect(inputs["stock_name"])["financials"]
    return {"financials": financials}

def sentiment_collection_node(inputs):
    agent = SocialSentimentAgent()
    comments = agent.collect(inputs["stock_name"])["comments"]
    return {"comments": comments}

def indices_collection_node(inputs):
    agent = MarketIndicesAgent()
    indices = agent.collect()["indices"]
    return {"indices": indices}

def merge_data_node(inputs):
    # Merge all collected data into a single dict
    merged = {
        "stock_name": inputs["stock_name"],
        "news": inputs["news"],
        "prices": inputs["prices"],
        "financials": inputs["financials"],
        "comments": inputs["comments"],
        "indices": inputs["indices"],
    }
    return {"data": merged}

def analysis_node(inputs):
    agent = AnalysisAgent()
    insights = agent.analyze(inputs["data"])
    return {"insights": insights}

def report_generation_node(inputs):
    agent = ReportGenerationAgent()
    report = agent.generate(inputs["insights"])
    return {"report": report}

def export_node(inputs):
    agent = ExportAgent()
    agent.export(inputs["report"], filename=f"{inputs['data']['stock_name']}_report.docx")
    return {"status": "exported"}

workflow = Workflow()
workflow.add_node(Node("news_collection", news_collection_node))
workflow.add_node(Node("price_collection", price_collection_node))
workflow.add_node(Node("financials_collection", financials_collection_node))
workflow.add_node(Node("sentiment_collection", sentiment_collection_node))
workflow.add_node(Node("indices_collection", indices_collection_node))
workflow.add_node(Node("merge_data", merge_data_node, after=["news_collection", "price_collection", "financials_collection", "sentiment_collection", "indices_collection"]))
workflow.add_node(Node("analysis", analysis_node, after=["merge_data"]))
workflow.add_node(Node("report_generation", report_generation_node, after=["analysis"]))
workflow.add_node(Node("export", export_node, after=["report_generation"]))

def run_workflow(stock_name):
    result = workflow.run({"stock_name": stock_name})
    return result

if __name__ == "__main__":
    stock_name = input("Enter stock name or ticker: ")
    run_workflow(stock_name)
    print("Workflow completed.")
