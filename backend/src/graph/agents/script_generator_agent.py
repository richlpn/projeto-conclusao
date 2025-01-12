from src.graph.agents.agent import Agent
from src.graph.output_parsers.codeblock_output_parser import PythonCodeParser


class ScriptGeneratorAgent(Agent):

    parser = PythonCodeParser()
