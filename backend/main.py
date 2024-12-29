from src.schema.data_source_schema import DataSourceSchema
from src.service.data_source_type_service import (
    get_data_source_type_service,
    get_data_source_type_repository,
)
from src.graph.output_parsers.schema_parser import DataSourceSchemaParser

serv = get_data_source_type_service(get_data_source_type_repository())
types = serv.get_all()
parser = DataSourceSchemaParser(types)

print(parser.get_format_instructions())
