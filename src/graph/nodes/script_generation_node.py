

from src.models.agents.script_generator_agent import SCRIPT_GENERATOR_AGENT
from src.models.data_docs_schemas_model import DataSourceSchema
from src.models.script_model import Script
from src.models.state import OverallState, ScriptGenerationState
from utils.llm_logger import LOGGER


def generate_python_script(state: OverallState) -> OverallState:

    generation_state = state["messages"][-1]
    if not isinstance(generation_state, ScriptGenerationState) or not isinstance(
        generation_state.pipeline_schema, DataSourceSchema
    ):
        raise ValueError("Last message should be a Generation State")

    schema = generation_state.pipeline_schema

    LOGGER.info(f"[WRITTING SCRIPT] - INPUT SCHEMA - {schema.name}")
    res = SCRIPT_GENERATOR_AGENT.invoke(
        {
            "SCHEMA": schema.model_dump_json(),
            "SCRIPT_DESCRIPTION": generation_state.pipeline_type.value,
        }
    )

    if not isinstance(res.content, str):
        raise ValueError("Chain must return a string")

    script = Script(raw_code=res.content, script_schema=schema)

    LOGGER.info(f"[CODE PARSER] - Finished - {script}")
    script.save()
    return OverallState(
        messages=[script.raw_code], origin=SCRIPT_GENERATOR_AGENT, destination="__end__"
    )
