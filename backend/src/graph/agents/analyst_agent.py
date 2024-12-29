from langchain_core.messages import AIMessage
from src.graph.agents.agent import Agent
from src.graph.tools.extract_docs_schema_tool import extract_schema_columns


class AnalystAgent(Agent[AIMessage]):
    tools = [extract_schema_columns]  # type: ignore


ANALYST = AnalystAgent()
