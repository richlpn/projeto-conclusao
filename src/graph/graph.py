from langgraph.graph import StateGraph

from src.models.state import OverallState

from .nodes import (
    new_data_source_event,
    tool_call,
    requirement_generation_event,
    generate_python_script,
)
from .routers import simple_tool_router

builder = StateGraph(OverallState)

builder.add_node("new_data_source", new_data_source_event)
builder.add_node("TOOL_CALL", tool_call)
builder.add_node("task_generation", requirement_generation_event)
builder.add_node("generate_python_script", generate_python_script)

builder.add_conditional_edges(
    "new_data_source", simple_tool_router, then="task_generation"
)
builder.add_edge("task_generation", "generate_python_script")
builder.set_entry_point("new_data_source")


GRAPH = builder.compile()
