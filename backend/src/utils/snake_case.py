def camel_to_snake(s):
    """
    Convert a camel case string to snake case.

    Args:
        s (str): The input string.

    Returns:
        str: The output string in snake case.

    Raises:
        TypeError: If the input is not a string.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    output = []
    for char in s:
        if char.isupper():
            output.append("_")
            output.append(char.lower())
        else:
            output.append(char)
    return "".join(output)
