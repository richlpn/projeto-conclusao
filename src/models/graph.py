import operator

from typing import Annotated, Literal, Sequence, TypedDict
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.messages import BaseMessage, ToolMessage, AIMessage


class GraphState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    origin: str

def agent_node(state:GraphState, agent: Runnable, config: RunnableConfig, name: str):
    result = agent.invoke(state)
    # We convert the agent output into a format that is suitable to append to the global state
    if not isinstance(result, ToolMessage):
        result = AIMessage(**result.dict(exclude={"type", "name"}), name=name)
    return GraphState(messages=[*state['messages'],result], origin=name)



def router(state: GraphState) -> Literal["call_tool", "__end__", "continue"]:
    # This is the router
    messages = state["messages"]
    last_message = messages[-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        # The previous agent is invoking a tool
        return "call_tool"
    if "PIPELINE FINALIZADA!" in last_message.content:
        return "__end__"
    return "continue"


