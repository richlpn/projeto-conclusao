# transform.py
from typing import Literal
from pydantic import BaseModel, Field


class TransformOperation(BaseModel):
    type: Literal["transform"] = Field(description="Type of operation.")
    function: str = Field(
        description="Transformation function (e.g., uppercase, lowercase, trim, replace)."
    )
    column: str = Field(description="Column to apply the transformation function to.")
    args: list[str] | None = Field(
        default=None,
        description="Additional arguments for the transformation function.",
    )
