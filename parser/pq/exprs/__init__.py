from ast import Try
from typing import TYPE_CHECKING

from ._base import Expression
from .add_sub import AddSubExpression
from .add_sub_unary import AddSubUnaryExpression
from .array import ArrayExpression
from .arrow import ArrowExpression
from .column import ColumnExpression
from .comparison import ComparisonExpression
from .concatenation import ConcatenationExpression
from .div_mul import DivMulExpression
from .each import EachExpression
from .function import FunctionExpression
from .identifier import BracketedIdentifierExpression, IdentifierExpression
from .if_expr import IfExpression
from .keyword import KeywordExpression
from .literal_number import LiteralNumberExpression
from .literal_string import LiteralStringExpression
from .meta import MetaExpression
from .and_or_expr import AndOrExpression
from .parens import ParenthesesExpression
from .record import RecordExpression
from .row import RowExpression
from .statement import StatementExpression
from .try_expr import TryExpression
from .type_expr import TypingExpression
from .variable import VariableExpression

if TYPE_CHECKING:
    from ..parser import Parser

"""
operators > all

operators:
if, comparison, concatenation, add/sub, div/mul, meta, add/sub, unary

variable > identifier
row > identifier
typing > keyword
arrow > parentheses
"""
EXPRESSION_HIERARCHY: tuple[type[Expression], ...] = (
    IfExpression,
    AndOrExpression,
    ComparisonExpression,
    ConcatenationExpression,
    AddSubExpression,
    DivMulExpression,
    MetaExpression,
    AddSubUnaryExpression,
    #
    ArrowExpression,
    TryExpression,
    ParenthesesExpression,
    StatementExpression,
    ColumnExpression,
    EachExpression,
    ArrayExpression,
    FunctionExpression,
    VariableExpression,
    RowExpression,
    TypingExpression,
    KeywordExpression,
    IdentifierExpression,
    RecordExpression,
    BracketedIdentifierExpression,
    LiteralStringExpression,
    LiteralNumberExpression,
)


def any_expression_match(parser: "Parser", skip_first: int = 0) -> Expression | None:
    """
    Matches any expression type.
    This is a utility function to simplify the matching process in other expressions.
    """
    for expr in EXPRESSION_HIERARCHY[skip_first:]:
        if match := expr.match(parser):
            return match
    return None


__all__ = [
    "Expression",
    "any_expression_match",
]
