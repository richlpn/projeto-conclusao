from langgraph.graph import StateGraph

from src.graph.routers.task_workflow_router import workflow_router
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
# builder.add_node("script_evaluation", evaluate_code_node)

builder.add_conditional_edges(
    "new_data_source", simple_tool_router, then="task_generation"
)
# builder.add_edge("task_generation", "generate_python_script")
builder.add_conditional_edges("task_generation", workflow_router)
builder.add_conditional_edges("generate_python_script", workflow_router)
# builder.add_conditional_edges("script_evaluation", workflow_router)

builder.set_entry_point("new_data_source")
builder.set_finish_point("generate_python_script")


GRAPH = builder.compile()
