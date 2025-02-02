from src.config.database.query_operator import QueryOperators


class InvalidQueryException(Exception):

    def __init__(self, signature: str, err: str) -> None:
        self.msg = (
            f"Query with signature `{signature}` is invalid! error description: {err}"
        )
        super().__init__(self.msg)


class InvalidQueryAtributeException(Exception):
    def __init__(self, attr: str, msg: str) -> None:
        self.msg = f"The attribute `{attr}` is invalid! {msg}"
        super().__init__(self.msg)


class InvalidOperationException(Exception):
    def __init__(self, operation: str) -> None:
        self.msg = f"The `{operation}` is not a part of {QueryOperators}"
        super().__init__(self.msg)
