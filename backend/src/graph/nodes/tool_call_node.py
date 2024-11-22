from langchain_core.messages import AIMessage
from langchain_core.runnables import Runnable

from src.models.state import OverallState
from src.utils.llm_logger import LOGGER


def __find_tool(tools: list, tool_name: str) -> Runnable:
    for tool in tools:
        if tool.name == tool_name:
            return tool

    raise ValueError("Tool with name {use_tool} not found on {agent}")


def tool_call(state: OverallState):
    msg = state["messages"][-1]
    agent = state["origin"]

    if not isinstance(msg, AIMessage):
        raise ValueError("Last message should be an AIMessage")

    if isinstance(agent, str) or (agent.tools is None):
        raise ValueError("No tools available for agent")

    tool = __find_tool(agent.tools, msg.tool_calls[-1]["name"])
    LOGGER.info(f"[TOOL CALL] - {msg.tool_calls[-1]['name']}")
    tool_answer = tool.invoke(input=msg.tool_calls[-1]["args"])
    return OverallState(
        messages=[tool_answer], origin="TOOL_CALL", destination="task_generation"
    )
