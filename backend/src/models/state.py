from enum import Enum
from operator import add
from typing import Annotated, Generic, TypedDict, TypeVar

from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field

from src.models.agents.agent import Agent
from src.schema.requirement_model import Requirement, Task


class PipelineStates(Enum):
    """
    Possible states of a pipeline."""

    EXTRACTION = """Your job is to create an extraction pipeline that includes the following steps:
      - Data source ingestion;
      - Data selection;
      - Column standardization (snake_case);
      - Incremental extraction setup;
      - Data validation;
      - logging"""
    TRANSFORMATION = 2
    LOAD = 3


S = TypeVar("S")


class OverallState(TypedDict):
    messages: Annotated[list[BaseMessage], add]
    origin: Agent | str
    destination: str


class ScriptGenerationState(BaseModel):
    requirements: Requirement
    task: Task | None = Field(
        default=None, description="Task that was completed, waiting for evaluation!"
    )
