import functools
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
    neighbor: Runnable


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

def registry_tools(agent: Runnable, workflow: StateGraph, tool_registry:dict[str,Runnable]):
    
    for tool in agent.tools: # type: ignore
        tool_registry[tool.name] = tool
        workflow.add_node(tool.name, tool)
        workflow.add_edge(agent.name, tool.name) # type: ignore
    return tool_registry


def create_use_tools(registered_tools:dict) -> Callable:

    def use_tools(state:GraphState) -> dict[str, list[AgentAction]]:
        tool_call = state['messages'][-1].tool_calls # type: ignore
        print(f"{tool_call['name']}.invoke(input={tool_call['args']})")
        tool = registered_tools[tool_call['name']]
        out = tool.invoke(input=tool_call['args'])
        
        action = AgentAction(tool=tool_call['name'],tool_input=tool_call['args'], log=str(out))
        return {"messages": [action]}
    
    return use_tools

def create_workflow(agents_graph: list[GraphNeighbor], ):
    TOOLS_REGISTRY = {}
    workflow = StateGraph(GraphState)
    for node in agents_graph:
        agent = node['origin']
        ag_node = functools.partial(agent_node, agent=agent, name=agent.name) # type: ignore
        workflow.add_node(agent.name, ag_node) # type: ignore
        registry_tools(agent, workflow, TOOLS_REGISTRY)
        # Cria uma conexão entre o agente e o router

        workflow.add_conditional_edges(
            agent.name, # type: ignore
            router) # type: ignore
    return create_use_tools(TOOLS_REGISTRY), workflow