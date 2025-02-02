from dataclasses import dataclass
from typing import Optional

from src.config.database.query_operator import QueryComparator, QueryOperators


@dataclass
class QueryExpr:
    value: str
    operation: QueryOperators
    depends: Optional[tuple[QueryComparator, "QueryExpr"]] = None

    def __str__(self) -> str:
        query = f"{self.value} {self.operation.value} %{self.value}%"
        if self.depends:
            comparator, depends_expr = self.depends
            query += f" {comparator.value} {depends_expr}"
        return query

    def build(self, model, *args, **values):
        col = getattr(model, self.value)
        args = list(args)
        try:
            val = values[self.value]
        except KeyError:
            if len(args) == 0:
                raise TypeError(f"missing argument: '{self.value}'")
            val = args.pop(0)
        query = self.operation.value(col, val)
        if not self.depends:
            return query
        comparator, depends_expr = self.depends
        query = comparator.value(query, depends_expr.build(model, *args, **values))
