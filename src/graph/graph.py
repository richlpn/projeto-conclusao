from langgraph.graph import StateGraph

from src.models.state import OverallState, ScriptGenerationState

from .nodes import new_data_source_event, tool_call
from .routers import simple_tool_router

builder = StateGraph(OverallState, output=ScriptGenerationState)

builder.add_node("new_data_source", new_data_source_event)
builder.add_node("TOOL_CALL", tool_call)

builder.add_conditional_edges("new_data_source", simple_tool_router)
builder.set_entry_point("new_data_source")


GRAPH = builder.compile()
