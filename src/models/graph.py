import operator

from typing import Annotated, Callable, Literal, Sequence, TypedDict
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.messages import BaseMessage, ToolMessage, AIMessage
from langchain_core.agents import AgentAction
from langgraph.graph import StateGraph, END

END_CALL_LOOP = 'PIPELINE FINALIZADA!'

class GraphState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    origin: str

class GraphNeighbor(TypedDict):
    origin: Runnable
    neighbors: list[Runnable]


def agent_node(state:GraphState, agent: Runnable, config: RunnableConfig, name: str):
    result = agent.invoke(state)
    # We convert the agent output into a format that is suitable to append to the global state
    if not isinstance(result, ToolMessage):
        result = AIMessage(**result.dict(exclude={"type", "name"}), name=name)
    return GraphState(messages=[result], origin=name)



def router(state: GraphState) -> str:
    # This is the router
    messages = state["messages"]
    last_message = messages[-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        # The previous agent is invoking a tool
        return last_message.tool_calls[0]['name']
    if END_CALL_LOOP in last_message.content:
        return "__end__"
    return "continue"

def registry_tools(agents: list[GraphNeighbor], workflow:StateGraph):
    TOOLS_REGISTRY = {}
    
    for node in agents:
        agent_tools = {}
        agent = node['origin']
        neighbors = {agent.name: n.name for n in node['neighbors']}

        for tool in agent.tools: # type: ignore
            TOOLS_REGISTRY[tool.name] = tool
            workflow.add_node(tool.name, tool)
            agent_tools[tool.name] = agent.name
            agent_tools[agent.name] = tool.name 

        workflow.add_conditional_edges(
            agent.name, # type: ignore
            router,
            {"continue": agents[i+1].name, "__end__": END, **neighbors}, # type: ignore
        )
    return TOOLS_REGISTRY

def create_use_tools(agents: list[Runnable], registered_tools:dict) -> Callable:
    
    def use_tools(state:GraphState) -> dict[str, list[AgentAction]]:
        tool_call = state['messages'][-1].tool_calls # type: ignore
        tool = registered_tools[tool_call['name']]
        out = tool.invoke(input=tool_call['args'])
        
        action = AgentAction(tool=tool_call['name'],tool_input=tool_call['args'], log=str(out))
        return {"messages": [action]}
    
    return use_tools
