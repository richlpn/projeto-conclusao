from langchain_core.output_parsers.base import BaseOutputParser

from src.schema.requirement_schema import RequirementSchema, TaskSchema
from src.utils.llm_logger import LOGGER
import json


class TaskOutputParser(BaseOutputParser[RequirementSchema]):
    def parse(self, text: str) -> RequirementSchema:
        text = text.replace("\n", "").strip()
        block = text[text.index("[") : text.rindex("]") + 1]
        block = json.loads(block)
        tasks = [
            TaskSchema(
                title=task["title"],
                description=task["description"],
                done_codition=task["done_condition"],
            )
            for task in block
        ]
        req = RequirementSchema(title="", tasks=tasks)
        return req

    def get_format_instructions(self) -> str:

        return "All tasks must be inside a triple backticks JSON block, for better formatting. A single task is a json with the fields 'title' and 'description' and 'done_condition'. You're expected to create multipe tasks. The 'description' field is a text describing what must be executed on the task."
