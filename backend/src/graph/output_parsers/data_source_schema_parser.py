import json
from typing import Iterable

from langchain_core.output_parsers.pydantic import _PYDANTIC_FORMAT_INSTRUCTIONS
from langchain_core.outputs import Generation
from src.graph.output_parsers.schema_parser import SchemaParser
from src.schema.data_source_column_schema import (
    DataSourceColumnUpdateSchema,
)
from src.schema.data_source_schema import (
    DataSourceSchema,
    DataSourceUpdateSchema,
)
from src.schema.data_source_type_schema import DataSourceTypeSchema


class DataSourceSchemaParser(SchemaParser):

    def __init__(self, types: Iterable[DataSourceTypeSchema]):
        super().__init__(name="DataSourceSchemaParser")
        self._types = types

    def insert_columns_property(self, schema: dict) -> dict:
        """
        Inserts the 'columns' property into the provided schema.

        This method modifies the input schema to include the definition of the 'columns' attribute,
        referencing the 'DataSourceColumnCreateSchema' type. The 'DataSourceColumnCreateSchema'
        definition is also added to the schema's '$defs' section.

        Args:
            schema (dict): The input schema to be modified.

        Returns:
            dict: The modified schema with the 'columns' property inserted.

        Raises:
            None
        """
        data_source_column_schema = DataSourceColumnUpdateSchema.model_json_schema()

        schema["$defs"] = {"DataSourceColumnUpdateSchema": data_source_column_schema}
        # Insert the definition of the attribute 'columns' at DataSourceSchema
        # The defition from DataSourceSchema references the type 'DataSourceColumnSchema'
        # So it must be replaced by the 'create schema'
        columns_schema = DataSourceSchema.model_json_schema()["properties"]["columns"]
        columns_schema["items"]["$ref"] = "#/$defs/DataSourceColumnUpdateSchema"

        schema["properties"]["columns"] = columns_schema
        return schema

    def insert_type_options(self, schema: dict) -> dict:
        options = {
            "description": "File type.",
            "anyOf": [
                {"type": "string", "value": data_source_type.name}
                for data_source_type in self._types
            ],
        }
        options["anyOf"].append({"type": None})
        schema["properties"]["type"] = options

        return schema

    def get_format_instructions(self) -> str:
        # Copy schema to avoid altering original Pydantic schema.
        # Filter the attributes with name 'id' or type 'uuid'
        data_source_schema = self.remove_id_properties(
            DataSourceUpdateSchema.model_json_schema()
        )

        # Insert the definition of a 'column create schema' so latter it's referenced as an attribute of the schema
        # Also replace the 'type' property by an list of options containing the 'name' of the type
        reduced_schema = self.insert_type_options(
            self.insert_columns_property(data_source_schema)
        )

        # Transforming the reduced schema into a refined string for token minimization
        schema_str = json.dumps(reduced_schema, ensure_ascii=False)

        # Insert the schema string on the basic concat prompt
        return _PYDANTIC_FORMAT_INSTRUCTIONS.format(schema=schema_str)

    def parse_result(self, result: list[Generation], *, partial: bool = False):
        schema = super().parse_result(result, partial=partial)
        for type in self._types:
            if type.name == schema["type"]:
                schema["type"] = type.id
        columns = [
            DataSourceColumnUpdateSchema.model_validate(column)
            for column in schema["columns"]
        ]
        schema = DataSourceUpdateSchema(
            name=schema["name"], type=schema["type"], separator=schema["separator"]
        )
        return schema, columns
