from langchain.agents import tool
from langchain_core.exceptions import OutputParserException


def extract_result_from_function(function_string: str) -> pd.DataFrame:
    """Executes a Python function from a string and returns the result as a Pandas DataFrame.
    Args:
        function_string (str): A string representing a Python function.
    Returns:
        pd.DataFrame: The result of the function execution as a Pandas DataFrame.
    Raises:
        OutputParserException: If the parser fails or returns a BaseMessage
    """
    result = eval(function_string)
    if not isinstance(result, pd.DataFrame):
        raise OutputParserException("Invalid result")
    return result


@tool(parse_docstring=True)
def evaluate_data_quality_tool(function_string) -> str:
    """Tool to read a data """
