from typing import Iterable
from src.graph.agents.agent import Agent
from src.graph.output_parsers.data_source_schema_parser import DataSourceSchemaParser
from src.schema.data_source_column_schema import DataSourceColumnUpdateSchema
from src.schema.data_source_schema import DataSourceUpdateSchema
from src.schema.data_source_type_schema import DataSourceTypeSchema


class SchemaExtractorAgent(
    Agent[tuple[DataSourceUpdateSchema, list[DataSourceColumnUpdateSchema]]]
):

    llm_name: str = "Schema Extractor Agent"

    def __init__(self, types: Iterable[DataSourceTypeSchema]) -> None:
        self.parser = DataSourceSchemaParser(types)
        super().__init__()
