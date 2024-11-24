from langchain_core.output_parsers.base import BaseOutputParser

from src.schema.requirement_model import Requirement, Task
from src.utils.llm_logger import LOGGER
import json


class TaskOutputParser(BaseOutputParser[Requirement]):
    def parse(self, text: str) -> Requirement:
        text = text.replace("\n", "").strip()
        block = text[text.index("[") : text.rindex("]") + 1]
        block = json.loads(block)
        tasks = [
            Task(
                title=task["title"],
                description=task["description"],
                done_codition=task["done_condition"],
            )
            for task in block
        ]
        req = Requirement(title="", tasks=tasks)
        return req

    def get_format_instructions(self) -> str:

        return "All tasks must be inside a triple backticks JSON block, for better formatting. A single task is a json with the fields 'title' and 'description' and 'done_condition'. You're expected to create multipe tasks. The 'description' field is a text describing what must be executed on the task."
