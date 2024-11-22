import json
from src.graph.graph import GRAPH
from src.graph.nodes.script_generation_node import generate_python_script
from src.models.requirement_model import Requirement, Task
from src.models.script.script_model import Script
from src.models.state import ScriptGenerationState

# %%
DOC = "./static/data/docs/Glossario - Arrecadação - Valores de Tributos e Preços Públicos_v1.txt"


def main():
    import json


from src.models.requirement_model import Requirement


def main():
    # Load the JSON data from the file
    with open("./static/data/task_output.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Parse the JSON data into the Requirement model
    tasks = map(lambda obj: Task(**obj), data["tasks"])
    requirement = Requirement(title=data["title"], tasks=tasks)

    state = ScriptGenerationState(requirements=requirement)
    script: Script = generate_python_script({"messages": [state]})[0]
    print(f"Script saved at - {script.save_to_temp_file()}")
