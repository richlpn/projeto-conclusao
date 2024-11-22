from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ToolCallAnswer(
    BaseModel,
    Generic[T],
):
    tool_name: str = Field(..., description="The name of the tool that was called.")
    input: str = Field(description="The input string")
    output: T = Field(description="The llm response")
