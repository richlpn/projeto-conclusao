from pydantic import BaseModel, Field


class FunctionState(BaseModel):
    name: str
    doc_string: str

    def __str__(self) -> str:
        return f"{self.name}:({self.doc_string})"


class ModuleState(BaseModel):
    imports: list[str] = Field(default_factory=list)
    functions: list[FunctionState] = Field(default_factory=list)
    raw: str = Field(default="")
