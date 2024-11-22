from src.models.agents.code_reviwer_agent import CodeReviwerAgent
from src.models.state import OverallState, ScriptGenerationState
from src.utils.llm_logger import LOGGER


def evaluate_code_node(state: OverallState) -> OverallState:

    generation_state = state["messages"][-1]

    if not isinstance(generation_state, ScriptGenerationState):
        raise ValueError("Last message should be a Generation State")

    task = generation_state.task

    review_agent = CodeReviwerAgent()
    if task is None or task.code is None:
        raise ValueError("Task should have code")
    LOGGER.info("[EVALUATING TASK] - %s", task.title)
    review = review_agent.invoke(TASK=task, CODE=task.code.code)
    task.review = review
    LOGGER.info("[REVIEW] - %s", task.review.status)

    return OverallState(
        messages=[generation_state], origin=review_agent, destination="__end__"
    )
