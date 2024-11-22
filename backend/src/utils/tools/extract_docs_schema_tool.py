from langchain.agents import tool
from src.graph.agents.schema_extractor_agent import SchemaExtractorAgent

from src.models.data_source import DataSource
from .read_file_tool import read_file_tool

schema_extractor_agent = SchemaExtractorAgent()


@tool(return_direct=True)
def extract_schema(path: str) -> DataSource:
    """Reads a documentation from a txt file and returns the schema.
    Args:
        path (str): Path to the txt file.
    Returns:
        DataSourceSchema: The schema of the data source.
    Rises:
        OutputParserException: If the parser fails or returns a BaseMessage
    """
    docs = read_file_tool.invoke(path).output
    schema = {}
    columns = {}

    for doc in docs:
        partial_schema = schema_extractor_agent.invoke(DOCUMENT=doc)

        if "name" not in schema:
            schema["name"] = partial_schema.name

        if "type" not in schema:
            schema["type"] = partial_schema.type

        for col in partial_schema.columns:
            if col.name in columns:
                continue
            columns[col.name] = col
    final_schema = DataSource(
        name=schema["name"], type=schema["type"], columns=list(columns.values())
    )
    return final_schema
