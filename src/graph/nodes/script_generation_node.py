from pkg_resources import Requirement
from src.models.agents.script_generator_agent import ScriptGeneratorAgent
from src.models.state import OverallState, ScriptGenerationState
from utils.llm_logger import LOGGER


def generate_python_script(state: OverallState) -> OverallState:

    generation_state = state["messages"][-1]
    if not isinstance(generation_state, ScriptGenerationState) or not isinstance(
        generation_state.requirements, Requirement
    ):
        raise ValueError("Last message should be a Generation State")

    while len(generation_state.requirements.tasks) > 0:
        task = generation_state.requirements.tasks.pop(0)
        agent = ScriptGeneratorAgent()

        LOGGER.info(f"[WRITTING SCRIPT] - CURRENT TASK - {task}")
        res = agent.invoke(TASK=task)

        if not isinstance(res, str):
            raise ValueError("Chain must return a string")

        generation_state.completed_tasks.tasks += [task]
        generation_state.code += [res]

    pipeline = "\n".join(generation_state.code)
    return OverallState(
        messages=[pipeline], origin=agent, destination="__end__"  # type: ignore
    )
