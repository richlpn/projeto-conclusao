from langchain_core.output_parsers import PydanticOutputParser

from src.models.agents.agent import Agent
from src.schema.requirement_schema import RequirementSchema
from src.output_parsers.tasks_output_parser import TaskOutputParser


class TaskCreationAgent(Agent[RequirementSchema]):
    name = "task_creation_agent"
    parser = PydanticOutputParser(
        name="TaskParsingOutput", pydantic_object=RequirementSchema
    )


TASK_CREATION_AGENT = TaskCreationAgent()
