from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.graph.agents.schema_extractor_agent import SchemaExtractorAgent
from src.schema.data_source_column_schema import DataSourceColumnUpdateSchema
from src.schema.data_source_schema import DataSourceCreateSchema, DataSourceSchema
from src.schema.data_source_type_schema import DataSourceTypeSchema


def extract_schema_columns(
    content: str, data_source_types: list[DataSourceTypeSchema]
) -> tuple[DataSourceCreateSchema, list[DataSourceColumnUpdateSchema]]:
    """Reads a documentation from a txt file and returns the schema.
    Args:
        path (str): Path to the txt file.
    Returns:
        DataSourceSchema: The schema of the data source.
    Rises:
        OutputParserException: If the parser fails or returns a BaseMessage
    """
    schema_extractor_agent = SchemaExtractorAgent(data_source_types)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_text(content)

    columns = {}
    partial_schemas = []
    for doc in texts:
        partial_schema, partial_columns = schema_extractor_agent.invoke(DOCUMENT=doc)
        partial_schemas.append(partial_schema)
        for column in partial_columns:
            if column.name and column.name not in columns:
                columns[column.name] = column

    fields = DataSourceCreateSchema.model_fields
    final_schema = {}
    for schema in partial_schemas:
        for field in fields:
            if getattr(schema, field) is not None:
                final_schema[field] = getattr(schema, field)
    return DataSourceCreateSchema.model_validate(final_schema), list(columns.values())
