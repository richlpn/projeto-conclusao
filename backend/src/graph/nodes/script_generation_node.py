from src.graph.agents.script_generator_agent import ScriptGeneratorAgent
from src.schema.task_schema import TaskCreateSchema


def generate_python_script(
    agent: ScriptGeneratorAgent, tasks: list[TaskCreateSchema]
) -> str:
    """
    Generate a script for the given task.

    Args:
        agent (ScriptGeneratorAgent): The agent to generate scripts with.
        req (Requirement): The task to generate a script for.
    Retuns:
        Script: The generated
    """
    tasks_dicts = [task.model_dump(exclude={"id", "data_source_id"}) for task in tasks]
    return agent.invoke(TASK=tasks_dicts, agent_scratchpad="")


__all__ = ["generate_python_script"]
