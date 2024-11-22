import json

from src.models.agents.task_creation_agent import TASK_CREATION_AGENT
from src.models.column import DataSource
from src.models.requirement_model import Requirement


def test_create_task_from_schema(path: str) -> Requirement:
    with open(path) as f:
        schema_data = json.load(f)
        schema = DataSource(**schema_data)
    x = TASK_CREATION_AGENT.invoke(SCHEMA=schema)

    with open("./static/data/task_output.json", "w") as f:
        json.dump(x.model_dump(), f, indent=4)
    return x


def main():
    test_create_task_from_schema("./static/data/schema_output.json")
