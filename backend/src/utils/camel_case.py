import re


def to_camel(string: str) -> str:
    if "_" not in string:
        return string
    words = string.split("_")
    words = [words[0]] + [word.capitalize() for word in words[1:]]
    return "".join(words)


def is_camel_case(s):
    """
    Check if a string is not in camel case.

    Args:
        s (str): The input string.

    Returns:
        bool: True if the string is in camel case, False otherwise.

    Raises:
        TypeError: If the input is not a string.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string")

    # Check if the string matches the camel case pattern
    pattern = r"^[a-z]+([A-Z][a-z]*)*$"
    return bool(re.match(pattern, s))
