import tempfile
import uuid
from functools import reduce

from pydantic import BaseModel, Field
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.models.script.function_model import Function
from src.config.database import Base


class Script(BaseModel):
    id: UUID = Field()
    code: str = Field(..., description="The script code")
    imports: list[str] = Field(default_factory=list)
    functions: list[Function] = Field(
        default_factory=list,
        description="List of function names and their descriptions",
    )

    # Define the ScriptSchema table
    class schema(Base):
        __tablename__ = "script_schemas"

        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        code = Column(String)
    
    @staticmethod
    def __extract_imports__(code: str) -> list[str]:
        """Extracts the imports from a python code string.
        Args:
            code (str): The python code to extract the imports from.
        Returns:
            A list of strings representing the imports in the given code.
        """
        clean = lambda x: (
            [x1.strip() for x1 in x.split(",")] if "," in x else [x.strip()]
        )
        imports = [
            line.split("import")[-1] for line in code.splitlines() if "import" in line
        ]
        imports = reduce(lambda ant, x: ant + x, map(clean, imports), list())

        return imports

    @classmethod
    def from_code_block(cls, code: str) -> "Script":
        """Creates a Script object from the given code.
        Args:
            code (str): The python code to extract the imports and functions from.
        Returns:
            A Script object with the extracted imports and functions.
        """

        # Extract imports
        imports = cls.__extract_imports__(code)
        funcs = Function.from_code_block(code)

        return cls(code=code, imports=imports, functions=funcs)

    def save_to_temp_file(self, suffix: str = ".py") -> str:
        """Saves the script code to a temporary file.

        Args:
            suffix (str): The file suffix. Defaults to ".py".

        Returns:
            The path to the saved temporary file.
        """
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp_file:
            # Write the script code to the temporary file
            tmp_file.write(self.code.encode("utf-8"))
            # Seek back to the beginning of the file for others to read it
            tmp_file.seek(0)
            return tmp_file.name
