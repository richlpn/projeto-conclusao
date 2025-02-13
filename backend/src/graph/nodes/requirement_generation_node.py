from src.models.agents.task_creation_agent import TASK_CREATION_AGENT
from src.models.column import DataSource
from src.models.state import OverallState, ScriptGenerationState
from src.utils.llm_logger import LOGGER


def requirement_generation_event(state: OverallState) -> OverallState:
    msg = state["messages"][-1]

    if not isinstance(msg, DataSource):
        raise ValueError("Message is not a data source schema")

    schema = msg.model_dump_json()
    LOGGER.info(
        f"[REQUIREMENT NODE] - Generating requirement for New data source - {msg.name},"
    )
    response = TASK_CREATION_AGENT.invoke(SCHEMA=schema)
    LOGGER.info(f"[REQUIREMENT NODE] - Generated {len(response.tasks)} Task(s).")
    response = ScriptGenerationState(requirements=response)
    return OverallState(
        messages=[response], origin=TASK_CREATION_AGENT, destination="__end__"  # type: ignore
    )
