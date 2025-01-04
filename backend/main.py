from uuid import UUID
from src.schema.data_source_schema import DataSourceSchema
from src.service.requirement_service import (
    get_requirement_service,
    get_requirement_repository,
    get_task_service,
    get_data_source_service,
)
from src.graph.output_parsers.tasks_output_parser import RequirementOutputParser

serv = get_requirement_service(
    get_requirement_repository(), get_task_service(), get_data_source_service()
)
print(
    RequirementOutputParser(
        data_source_id=UUID("0c1ecd73-266a-406b-87f3-7003a063403b")
    ).get_format_instructions()
)
