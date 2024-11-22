from src.models.agents.agent import Agent
from src.output_parsers.codeblock_output_parser import PythonCodeParser


class ScriptGeneratorAgent(Agent):

    parser = PythonCodeParser()
