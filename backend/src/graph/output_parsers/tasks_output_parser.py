import json
from typing import Type
from uuid import UUID

from langchain_core.output_parsers.pydantic import _PYDANTIC_FORMAT_INSTRUCTIONS
from langchain_core.outputs import Generation
from pydantic import Field
from src.graph.output_parsers.schema_parser import SchemaParser
from src.schema.requirement_schema import RequirementCreateFromLLMSchema
from src.schema.task_schema import TaskCreateSchema


class RequirementOutputParser(SchemaParser[RequirementCreateFromLLMSchema]):

    data_source_id: UUID = Field()
    pydantic_object: Type[RequirementCreateFromLLMSchema] = Field(
        default=RequirementCreateFromLLMSchema
    )

    def parse_result(self, result: list[Generation], *, partial: bool = False):
        schema = super().parse_result(result, partial=partial)
        tasks = [
            TaskCreateSchema.model_validate(
                {**task, "data_source_id": self.data_source_id}
            )
            for task in schema["tasks"]
        ]
        req = RequirementCreateFromLLMSchema(tasks=tasks)
        return req

    def get_format_instructions(self) -> str:
        data_source_schema = self.remove_id_properties(
            self.pydantic_object.model_json_schema()
        )

        # Transforming the reduced schema into a refined string for token minimization
        schema_str = json.dumps(data_source_schema, ensure_ascii=False)

        # Insert the schema string on the basic concat prompt
        return _PYDANTIC_FORMAT_INSTRUCTIONS.format(schema=schema_str)
