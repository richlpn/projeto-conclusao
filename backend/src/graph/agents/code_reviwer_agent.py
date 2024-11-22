from langchain_core.messages import AIMessage
from src.models.agents.agent import Agent
from src.output_parsers.review_output_parser import ReviewOutputParser


class CodeReviwerAgent(Agent):
    parser = ReviewOutputParser()


reviwer_agent = CodeReviwerAgent()
