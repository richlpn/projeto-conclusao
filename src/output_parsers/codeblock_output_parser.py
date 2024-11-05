import re
from functools import reduce

from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import BaseOutputParser

from src.models.script_model import Script


class PythonCodeParser(BaseOutputParser):

    def __extract_imports__(self, code: str) -> list[str]:
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

    def __get_functions__(self, code: str) -> list[tuple[str, str]]:
        """Find the functions definitions on a code block and their docstring.
        Args:
            code (str): The code to parse for function definitions.
        Returns:
            tuple[str, str]: A dictionary of function name to docstring.
        """

        # Find all function definitions in the code string.
        pattern = r"def\s+(\w+)|(\"\"\"([\s\S]*?)\"\"\")"
        func_defs = re.findall(pattern, code)
        funcs = [
            (func_defs[i][0], func_defs[i + 1][1]) for i in range(0, len(func_defs), 2)
        ]
        # get function name and docstring from each definition.
        return funcs

    def parse(self, text: str):
        # Extract the code from the response, assuming it's enclosed in triple quotes (```python ... ```)
        code_start = text.find("```python")
        code_end = text.find("```", code_start + 1)

        if code_start == -1 or code_end == -1:
            raise OutputParserException("No code block found.")

        # Extract the code and remove the ```python markers
        python_code = text[code_start + len("```python") : code_end].strip()
        imports = self.__extract_imports__(python_code)
        functions = self.__get_functions__(python_code)

        return Script(code=python_code, imports=imports, functions=functions)

    def get_format_instructions(self):
        return "The output should be a valid Python code block enclosed in triple backticks (```python ... ```)."
