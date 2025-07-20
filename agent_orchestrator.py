# agent_orchestrator.py
"""
Main orchestrator for the agent-based stock report generation app.
"""

from agents.agents import DataCollectionAgent, AnalysisAgent, ReportGenerationAgent, ExportAgent
import os
import json

class OrchestratorAgent:
    def __init__(self):
        self.data_agent = DataCollectionAgent()
        self.analysis_agent = AnalysisAgent()
        self.report_agent = ReportGenerationAgent()
        self.export_agent = ExportAgent()

    def generate_stock_report(self, stock_name: str):
        # Step 1: Data Collection
        data = self.data_agent.collect(stock_name)
        # Save collected data for review/debug
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        data_path = os.path.join(output_dir, f"{stock_name}_collected.json")
        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Collected data saved to {data_path}")
        # Step 2: Analysis
        insights = self.analysis_agent.analyze(data)
        # Step 3: Report Generation
        report = self.report_agent.generate(insights)
        # Step 4: Export
        self.export_agent.export(report, filename=f"{stock_name}_report.docx")
        print(f"Report for {stock_name} generated successfully.")

if __name__ == "__main__":
    stock_name = input("Enter stock name or ticker: ")
    orchestrator = OrchestratorAgent()
    orchestrator.generate_stock_report(stock_name) 