import re

from langchain_core.output_parsers.base import BaseOutputParser

from src.models.requirement_model import Requirement, Task
from src.utils.llm_logger import LOGGER
import json


class TaskOutputParser(BaseOutputParser[Requirement]):
    def parse(self, text: str) -> Requirement:
        text = text.replace("\n", "").strip()
        block = text[text.index("[") : text.index("]") + 1]
        block = json.loads(block)
        tasks = [Task(**task) for task in block]
        req = Requirement(title="", tasks=tasks)
        return req

    def get_format_instructions(self) -> str:

        return """All tasks must be inside a triple backticks block, for better formatting.
        A single task is a json with the fields title and description. You're expected to create multipe tasks.
        Here are some examples of tasks descriptions:
        ```json
        [
            {
            "title": "Read data source",
            "description" : "Use the `SAILES_PATH` environment variable to get the path ofte if the file on the pathan ValueError with message 'File extention not suported by this .read_csv to load the dataframe."
            },
            {
            "title":"Standarize columns",
            "description" : "Check if the following columns are present, Raise an Excepiton with the message 'Missing required columns':customerId, orderDate, productCode, totalAmountPaid, shippingAddressWrite a function 'parse_columns' that takes a string and transforms then into sxample customerId -> customer_id; order_date -> proarse_columns' to transform the all the columns."
            },
            {
            "title":"Load the processed dataframe",
            "description" : "Load the dataframe using the path at `SAILES_OUTPUT_PATH` as parquet file."
            }
        ]
        ```
       """
