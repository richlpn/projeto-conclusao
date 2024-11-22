from typing import Literal
from pydantic import BaseModel, Field


class JoinOperation(BaseModel):
    type: Literal["join"] = Field(description="Type 'Join' of operation.")
    tables: list[str] = Field(description="Tables involved in the join operation.")
    on: str = Field(description="Column to join on.")
