from ast import IfExp
from typing import TYPE_CHECKING

from ._base import Expression
from .array import ArrayExpression
from .column import ColumnExpression
from .comparison import ComparisonExpression
from .function import FunctionExpression
from .identifier import IdentifierExpression
from .if_expr import IfExpression
from .keyword import KeywordExpression
from .literal_number import LiteralNumberExpression
from .literal_string import LiteralStringExpression
from .type_expr import TypingExpression
from .variable import VariableExpression

if TYPE_CHECKING:
    from ..parser import Parser
EXPRESSION_HIERARCHY: tuple[type[Expression], ...] = (
    # operators must come first
    IfExpression,
    ComparisonExpression,
    #
    ColumnExpression,
    ArrayExpression,
    FunctionExpression,
    VariableExpression,  # must be before IdentifierExpression
    IdentifierExpression,
    LiteralStringExpression,
    LiteralNumberExpression,
    TypingExpression,  # must be before KeywordExpression
    KeywordExpression,
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
