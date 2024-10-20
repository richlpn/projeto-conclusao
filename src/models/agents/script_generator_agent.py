
from langchain.output_parsers import PydanticOutputParser
from src.models.agents.agent import Agent


class ScriptGeneratorAgent(Agent):

    parser: PydanticOutputParser