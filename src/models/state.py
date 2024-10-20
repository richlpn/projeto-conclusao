from enum import Enum
from operator import add
from typing import Annotated, Generic, TypedDict, TypeVar

from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field

from src.models.agents.agent import Agent


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


class ScriptGenerationState(
    BaseModel,
    Generic[S],
):
    pipeline_schema: S | str
    pipeline_type: PipelineStates = Field(default=PipelineStates.EXTRACTION)
    error_count: int = Field(default=0)
    origin: str
    destination: str
