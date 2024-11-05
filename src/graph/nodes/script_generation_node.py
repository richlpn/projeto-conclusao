from src.models.agents.script_generator_agent import ScriptGeneratorAgent
from src.models.module_state import FunctionState, ModuleState
from src.models.requirement_model import Requirement, Task
from src.models.script_model import Script
from src.models.state import OverallState, ScriptGenerationState
from src.utils.llm_logger import LOGGER


def __process_script__(
    agent: ScriptGeneratorAgent, task: Task, current_script_state: str
) -> Script:
    """
    Generate a script for the given task.

    Args:
        agent (ScriptGeneratorAgent): The agent to generate scripts with.
        task (Task): The task to generate a script for.
        current_script_state (str): A description of the current functions/imports on the module.
    Retuns:
        Script: The generated
    """

    LOGGER.info(f"[WRITTING SCRIPT] - CURRENT TASK - {task}")
    res = agent.invoke(TASK=task, MODULE_STATE=current_script_state)

    return res


def __get_module_state__(module: ModuleState, is_new: bool):

    if is_new:
        return "This is a new empty python module."

    imports = ",".join(module.imports)
    functions = "\n".join(map(str, module.functions))
    return f"The current python module content is:\nImports\n{imports}\nFuctions:\n{functions}"


def __update_module_state__(module: ModuleState, new_script: Script):

    functions = [
        FunctionState(name=fn[0], doc_string=fn[1]) for fn in new_script.functions
    ]
    module.functions.extend(functions)

    module.imports = list(set(new_script.imports + module.imports))
    module.raw += new_script.code

    return module


def generate_python_script(state: OverallState) -> OverallState:

    generation_state = state["messages"][-1]

    if not isinstance(generation_state, ScriptGenerationState) or not isinstance(
        generation_state.requirements, Requirement
    ):
        raise ValueError("Last message should be a Generation State")

    module = ModuleState()

    while len(generation_state.requirements.tasks) > 0:
        task = generation_state.requirements.tasks.pop(0)
        agent = ScriptGeneratorAgent()
        state_description = __get_module_state__(
            module, len(generation_state.code) == 0
        )

        script = __process_script__(agent, task, state_description)
        module = __update_module_state__(module, script)

    return OverallState(
        messages=[module], origin=agent, destination="__end__"  # type: ignore
    )


__all__ = ["generate_python_script"]
