import os
from datetime import datetime

from pydantic import BaseModel, Field

from src.models.data_docs_schemas_model import DataSourceSchema


class Script(BaseModel):

    creation_date: datetime = Field(default_factory=datetime.now, init=False)
    raw_code: str = Field(repr=False)
    path: str = Field(default="./outputs/")
    script_schema: DataSourceSchema = Field()

    def save_raw(self, filename: str):
        with open(filename, "w") as f:
            f.write(self.raw_code)

    def save_processed(self, filename: str):
        with open(filename, "w") as f:
            f.write(self.process_code)

    @property
    def process_code(self):

        if getattr(self, "_processed_code", None) is not None:
            return self._processed_code

        code = self.raw_code.split("```")
        code = code[1].replace("python", "")
        self._processed_code = code
        return self._processed_code

    def save(self):
        raw_filename = os.path.join(
            self.path, "raw/", f"{self.creation_date:%Y_%m_%d_%H%M}.py"
        )
        processed_filename = os.path.join(
            self.path, "processed/", f"{self.creation_date:%Y_%m_%d_%H%M}.py"
        )
        self.save_raw(raw_filename)
        self.save_processed(processed_filename)
