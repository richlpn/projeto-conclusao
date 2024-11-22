import re
from pydantic import BaseModel


class Function(BaseModel):
    name: str
    doc_string: str

    def __str__(self) -> str:
        return f"{self.name}:({self.doc_string})"

    @staticmethod
    def __get_functions__(code: str) -> list[tuple[str, str]]:
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
            # (func_defs[i][0], func_defs[i + 1][1]) for i in range(0, len(func_defs), 2)
        ]
        # get function name and docstring from each definition.
        return funcs

    @classmethod
    def from_code_block(cls, code: str) -> list["Function"]:
        """Creates a new instance of the class from a python code block string.
        Args:
            code (str): The code to parse for function definitions.
        Returns:
            A new instance of the class.
        """
        functions = cls.__get_functions__(code)

        return [cls(name=fn[0], doc_string=fn[1]) for fn in functions]
