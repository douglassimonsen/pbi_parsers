from typing import TYPE_CHECKING

from ..tokens import TokenType
from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from ..parser import Parser


class NotExpression(Expression):
    expr: Expression

    def __init__(
        self,
        expr: Expression,
    ):
        self.expr = expr

    def pprint(self) -> str:
        return f"Not ({self.expr.pprint()})"

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "NotExpression | None":
        from . import any_expression_match

        if parser.consume().type != TokenType.NOT:
            return None

        expr = any_expression_match(parser)
        if expr is None:
            return None
        return NotExpression(expr=expr)
