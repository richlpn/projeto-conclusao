from langgraph.graph import END

from src.models.agents.analyst_agent import ANALYST
from src.models.state import OverallState
from src.utils.llm_logger import LOGGER


def new_data_source_event(state: OverallState) -> OverallState:
    LOGGER.info(f"[NEW DATA EVENT] - Started from - {state['origin']}")
    response = ANALYST.invoke(input=state["messages"][-1])

    destination = END
    if response.tool_calls:
        destination = "TOOL_CALL"
    return OverallState(messages=[response], origin=ANALYST, destination=destination)
