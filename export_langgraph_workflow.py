from langgraph.graph import StateGraph
import matplotlib.pyplot as plt
import networkx as nx
import os

def get_workflow_edges():
    # Define the workflow structure as (from, to) edges
    edges = [
        ("news_collection", "merge_data"),
        ("price_collection", "merge_data"),
        ("financials_collection", "merge_data"),
        ("sentiment_collection", "merge_data"),
        ("indices_collection", "merge_data"),
        ("merge_data", "analysis"),
        ("analysis", "report_generation"),
        ("report_generation", "export"),
    ]
    return edges

def export_workflow_graph_pdf(filepath="output/langgraph_workflow.pdf"):
    edges = get_workflow_edges()
    g = nx.DiGraph()
    for src, dst in edges:
        g.add_edge(src, dst)
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(g)
    nx.draw(g, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_weight='bold', edge_color='gray', arrows=True)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    plt.savefig(filepath, format="pdf")
    plt.close()
    print(f"LangGraph workflow graph exported to {filepath}")

if __name__ == "__main__":
    export_workflow_graph_pdf()
