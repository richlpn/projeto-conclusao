from functools import wraps
from typing import Callable

from sqlalchemy import and_, or_
from inspect import signature

from src.config.database.handle_query_exception import handle_sqlalchemy_session
from src.config.database.query_expression import QueryExpr
from src.config.database.query_operator import QueryComparator, QueryOperators
from src.exceptions.query_execptions import (
    InvalidOperationException,
    InvalidQueryAtributeException,
    InvalidQueryException,
)
from src.utils.camel_case import is_camel_case
from src.utils.snake_case import camel_to_snake


def built_query_expr(partial_body: list[str]) -> tuple[QueryExpr, list[str]]:
    partial_body = partial_body.copy()
    attr = partial_body.pop(0)
    op = partial_body.pop(0)
    if op == "not":
        op = "not_" + partial_body.pop(0)

    not_ops = {
        "not_eq": QueryOperators.NEQ,
        "not_gt": QueryOperators.LTE,
        "not_lt": QueryOperators.GTE,
    }

    if not is_camel_case(attr):
        raise InvalidQueryAtributeException(attr, "Attribute must be in camel case")

    attr = camel_to_snake(attr)
    print("ATTRIBUTE", attr)
    try:
        operation = not_ops[op] if op in not_ops else QueryOperators[op.upper()]
        return QueryExpr(attr, operation), partial_body
    except KeyError as e:
        raise InvalidOperationException(op)


def parser(signature: str) -> QueryExpr:
    """Takes a function signature and returns a tuple of operations and comparators to be executed."""

    if not signature.startswith("filter_by_"):
        raise InvalidQueryException(signature, "Signature must start with `filter_by`")

    # Get the body to create the operation
    body = signature.removeprefix("filter_by_").split("_")
    expression: list[QueryExpr] = []

    if len(body) == 1:
        return QueryExpr(camel_to_snake(body[0]), QueryOperators.EQ)
    i = 0
    while len(body) > 0:
        # Does this query starts with an comparation?
        # If so save it and go to the next part of the body
        # If not, it must be an attribute
        try:
            cmp = QueryComparator[body[i].upper()]
            i += 1
        except KeyError:
            cmp = None
        try:
            expr, body = built_query_expr(body[i:])
            if len(expression) == 0 and cmp:
                raise InvalidQueryException(
                    signature, f"Signature cannot start with comparator `{body[i]}`"
                )
            if cmp:
                expr.depends = (cmp, expression[-1])
        except InvalidOperationException as err:
            raise InvalidQueryException(signature, str(err)) from err
        expression.append(expr)

    return expression[-1]


def query(func: Callable) -> Callable:
    """
    Decorator that generates SQLAlchemy queries based on function names.
    Supports operations: eq, gt, lt, not_eq
    Format: filter_by_[field]_[operation]_[field]_[operation]_[logic]
    Example: filter_by_age_gt_and_salary_lt
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        func_name = func.__name__
        filters_expression = parser(func_name)
        sig = signature(func)
        bound_args = sig.bind(self, *args, **kwargs)
        bound_args.apply_defaults()

        return (
            self.db.query(self.model)
            .filter(filters_expression.build(self.model, *args, **kwargs))
            .all()
        )

    return handle_sqlalchemy_session(wrapper)
