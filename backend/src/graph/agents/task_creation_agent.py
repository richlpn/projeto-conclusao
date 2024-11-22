from langchain_core.output_parsers import PydanticOutputParser

from src.models.agents.agent import Agent
from src.models.requirement_model import Requirement
from src.output_parsers.tasks_output_parser import TaskOutputParser


class TaskCreationAgent(Agent[Requirement]):
    name = "task_creation_agent"
    parser = PydanticOutputParser(name="TaskParsingOutput", pydantic_object=Requirement)


TASK_CREATION_AGENT = TaskCreationAgent()
