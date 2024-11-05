from typing import Literal
from src.models.state import OverallState


def simple_tool_router(
    state: OverallState,
) -> Literal["TOOL_CALL"] | Literal["task_generation"]:
    if state["destination"] == "TOOL_CALL":
        return "TOOL_CALL"
    return "task_generation"
