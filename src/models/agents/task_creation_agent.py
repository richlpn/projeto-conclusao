from src.models.agents.agent import Agent
from src.models.requirement_model import Requirement
from src.output_parsers.tasks_output_parser import TaskOutputParser


class TaskCreationAgent(Agent[Requirement]):
    name = "task_creation_agent"
    parser = TaskOutputParser()


TASK_CREATION_AGENT = TaskCreationAgent()
