from typing import Literal
from pydantic import BaseModel, Field


class FilterOperation(BaseModel):
    type: Literal["filter"] = Field(description="Type 'Filter' of operation.")
    condition: str = Field(description="Filter condition.")
