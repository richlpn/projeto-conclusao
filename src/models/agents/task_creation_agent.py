from langchain.output_parsers import PydanticOutputParser

from src.models.agents.agent import Agent
from src.models.requirement_model import Requirement


class TaskCreationAgent(Agent):

    name = "task_creation_agent"
    parser: PydanticOutputParser[Requirement] = PydanticOutputParser(
        pydantic_object=Requirement
    )


TASK_CREATION_AGENT = TaskCreationAgent()
