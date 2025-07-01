import textwrap
from typing import TYPE_CHECKING

from ..tokens import TokenType
from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from ..parser import Parser


class EachExpression(Expression):
    each_expr: Expression

    def __init__(self, each_expr: Expression):
        self.each_expr = each_expr

    def pprint(self) -> str:
        each_expr = textwrap.indent(self.each_expr.pprint(), " " * 10)[10:]
        base = f"""
Each (
    each: {each_expr},
)""".strip()
        return base

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "EachExpression | None":
        from . import any_expression_match

        _each = parser.consume()
        if _each.type != TokenType.EACH:
            return None
        each_expr: Expression | None = any_expression_match(parser)
        if not each_expr:
            return None
        return EachExpression(each_expr=each_expr)
