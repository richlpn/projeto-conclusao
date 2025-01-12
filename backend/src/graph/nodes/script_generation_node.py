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
    codes = []
    for task in tasks:
        if "feature integrations" in task.title.lower():
            res = agent.invoke(TASK=task, CODE="\n".join(codes), agent_scratchpad="")
            return res.code
        res = agent.invoke(TASK=task, CODE="", agent_scratchpad="")
        codes.append(res.code)

    return "\n".join(codes)


__all__ = ["generate_python_script"]
