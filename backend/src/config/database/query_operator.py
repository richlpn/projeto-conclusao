import operator
from enum import Enum

from sqlalchemy import and_, or_


class QueryOperators(Enum):
    GT = operator.gt
    LT = operator.lt
    EQ = operator.eq
    IN = operator.contains
    NEQ = operator.ne
    NOT = operator.not_
    LTE = operator.le
    GTE = operator.ge


class QueryComparator(Enum):
    AND = and_
    OR = or_
