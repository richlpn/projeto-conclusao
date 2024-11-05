import os
from datetime import datetime

from pydantic import BaseModel, Field

from src.models.data_docs_schemas_model import DataSourceSchema


class Script(BaseModel):

    code: str = Field(..., description="The script code")
    imports: list[str]
    functions: list[tuple[str, str]] = Field(
        default_factory=list,
        description="List of function names and their descriptions",
    )
