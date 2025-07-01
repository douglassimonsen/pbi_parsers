from typing import TYPE_CHECKING

from ._base import Expression
from .function import FunctionExpression
from .keyword import KeywordExpression
from .literal_string import LiteralStringExpression

if TYPE_CHECKING:
    from ..parser import Parser
EXPRESSION_HIERARCHY: tuple[type[Expression], ...] = (
    FunctionExpression,
    LiteralStringExpression,
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
    breakpoint()
    return None


__all__ = [
    "Expression",
    "any_expression_match",
]
