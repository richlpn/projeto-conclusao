from src.models.agents.task_creation_agent import TASK_CREATION_AGENT
from src.models.data_docs_schemas_model import DataSourceSchema
from src.models.state import OverallState
from src.utils.llm_logger import LOGGER


def requirement_generation_event(state: OverallState) -> OverallState:
    msg = state["messages"][-1]

    if not isinstance(msg, DataSourceSchema):
        raise ValueError("Message is not a data source schema")

    schema = msg.model_dump_json()
    LOGGER.info(
        f"[REQUIREMENT NODE] - Generating requirement for New data source - {msg.name},"
    )
    response = TASK_CREATION_AGENT.invoke(SCHEMA=schema)
    LOGGER.info(f"[REQUIREMENT NODE] - Generated {len(response.tasks)} Task(s).")
    return OverallState(
        messages=[response], origin=TASK_CREATION_AGENT, destination="__end__" # type: ignore
    )
