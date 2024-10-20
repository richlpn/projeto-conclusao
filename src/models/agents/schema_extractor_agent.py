from langchain_core.output_parsers import PydanticOutputParser
from src.models.agents.agent import Agent
from src.models.data_docs_schemas_model import DataSourceSchema


class SchemaExtractorAgent(Agent[DataSourceSchema]):

    name: str = "Schema Extractor Agent"
    parser = PydanticOutputParser(
        name="Data source Schema parser", pydantic_object=DataSourceSchema
    )
