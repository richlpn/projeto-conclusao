from langchain_core.output_parsers import PydanticOutputParser
from src.models.agents.agent import Agent
from src.models.data_docs_schemas_model import DataSource


class SchemaExtractorAgent(Agent[DataSource]):

    name: str = "Schema Extractor Agent"
    parser = PydanticOutputParser(
        name="Data source Schema parser", pydantic_object=DataSource
    )
