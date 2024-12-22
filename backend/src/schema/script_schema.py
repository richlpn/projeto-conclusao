import uuid

from pydantic import BaseModel, Field
from sqlalchemy.dialects.postgresql import UUID
from src.config.database import Base


class Script(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    code: str = Field(..., description="The python script code")

    @classmethod
    def from_code_block(cls, code: str) -> "Script":
        """Creates a Script object from the given code.
        Args:
            code (str): The python code to extract the imports and functions from.
        Returns:
            A Script object with the extracted imports and functions.
        """

        # Extract imports

        return cls(code=code)
