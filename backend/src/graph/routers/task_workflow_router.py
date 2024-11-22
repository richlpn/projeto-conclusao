from typing import Literal
from src.models.review_model import ReviewStatus
from src.models.state import OverallState, ScriptGenerationState


def workflow_router(
    state: OverallState,
) -> Literal["generate_python_script", "__end__"]:

    last_msg = state["messages"][-1]

    if isinstance(last_msg, ScriptGenerationState):
        return "generate_python_script"

    return "__end__"
