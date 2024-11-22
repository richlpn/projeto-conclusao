from typing import Literal
from pydantic import BaseModel, Field


class AggregateOperation(BaseModel):
    type: Literal["aggregate"] = Field(description="Type of operation.")
    function: str = Field(description="Aggregate function (e.g., sum, avg, count).")
    column: str = Field(description="Column to apply the aggregate function to.")
    groupBy: str | None = Field(default=None, description="Column to group by.")
