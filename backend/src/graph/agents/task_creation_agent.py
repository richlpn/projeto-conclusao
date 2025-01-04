from uuid import UUID

from src.graph.agents.agent import Agent
from src.graph.output_parsers.tasks_output_parser import RequirementOutputParser
from src.schema.requirement_schema import RequirementCreateFromLLMSchema


class TaskCreationAgent(Agent[RequirementCreateFromLLMSchema]):
    name = "task_creation_agent"

    def __init__(self, id: UUID) -> None:
        self.parser = RequirementOutputParser(data_source_id=id)
        super().__init__()
