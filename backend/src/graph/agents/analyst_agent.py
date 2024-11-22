from langchain_core.messages import AIMessage

from src.models.agents.agent import Agent
from src.tools.extract_docs_schema_tool import extract_schema


class AnalystAgent(Agent[AIMessage]):
    tools = [extract_schema]  # type: ignore


ANALYST = AnalystAgent()
