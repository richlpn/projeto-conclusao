from langchain.agents import tool
from langchain_core.exceptions import OutputParserException

from src.models.agents.schema_extractor_agent import SchemaExtractorAgent

from ..models.data_docs_schemas_model import DataSourceSchema
from .read_file_tool import read_file_tool

schema_extractor_agent = SchemaExtractorAgent()


@tool(return_direct=True)
def extract_schema(path: str) -> DataSourceSchema:
    """Reads a documentation from a txt file and returns the schema.
    Args:
        path (str): Path to the txt file.
    Returns:
        DataSourceSchema: The schema of the data source.
    Rises:
        OutputParserException: If the parser fails or returns a BaseMessage
    """
    docs = read_file_tool.invoke(path)
    schema = schema_extractor_agent.invoke(DOCUMENT=docs)
    if not isinstance(schema, DataSourceSchema):
        raise OutputParserException("Invalid Schema")
    return schema
