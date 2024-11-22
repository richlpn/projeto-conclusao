from pydantic import BaseModel, Field


class DataSourceColumnDTO(BaseModel):
    type: str = Field(description="Column type.")
    name: str = Field(description="Column name.")
    description: str = Field(description="Column brief description (used for context)")
