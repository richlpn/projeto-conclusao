from src.models.agents.script_generator_agent import ScriptGeneratorAgent
from src.models.requirement_model import Requirement, Task
from src.models.script.script_model import Script
from src.models.state import OverallState, ScriptGenerationState
from src.utils.llm_logger import LOGGER


def __process_script__(agent: ScriptGeneratorAgent, req: Requirement) -> Script:
    """
    Generate a script for the given task.

    Args:
        agent (ScriptGeneratorAgent): The agent to generate scripts with.
        req (Requirement): The task to generate a script for.
    Retuns:
        Script: The generated
    """
    codes = []
    tasks = req.tasks
    for task in tasks:
        LOGGER.info("[SOLVING TASK] - %s", task.title)
        res = agent.invoke(TASK=task, CODE="", agent_scratchpad="")
        codes.append(res.code)

    return agent.invoke(TASK=Task(), CODE="\n".join(codes))


def generate_python_script(state: OverallState) -> OverallState:

    generation_state = state["messages"][-1]

    if not isinstance(generation_state, ScriptGenerationState):
        raise ValueError("Last message should be a Generation State")

    # task = generation_state.requirements.get_task()
    agent = ScriptGeneratorAgent()
    code = __process_script__(
        agent,
        generation_state.requirements,
    )
    return OverallState(messages=[code], origin=agent, destination="")  # type: ignore


__all__ = ["generate_python_script"]
