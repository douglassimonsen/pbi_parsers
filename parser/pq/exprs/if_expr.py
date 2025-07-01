import textwrap
from typing import TYPE_CHECKING

from ..tokens import TokenType
from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from ..parser import Parser


class IfExpression(Expression):
    if_expr: Expression
    then_expr: Expression
    else_expr: Expression

    def __init__(
        self, if_expr: Expression, then_expr: Expression, else_expr: Expression
    ):
        self.if_expr = if_expr
        self.then_expr = then_expr
        self.else_expr = else_expr

    def pprint(self) -> str:
        if_expr = textwrap.indent(self.if_expr.pprint(), " " * 10)[10:]
        then_expr = textwrap.indent(self.then_expr.pprint(), " " * 10)[10:]
        else_expr = textwrap.indent(self.else_expr.pprint(), " " * 10)[10:]
        base = f"""
If (
    if: {if_expr},
    then: {then_expr},
    else: {else_expr}
)""".strip()
        return base

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "IfExpression | None":
        from . import any_expression_match

        _if = parser.consume()
        if _if.type != TokenType.IF:
            return None
        if_expr: Expression | None = any_expression_match(
            parser
        )  # this expression can recurse
        if not if_expr:
            return None

        _then = parser.consume()
        if _then.type != TokenType.THEN:
            return None
        then_expr = any_expression_match(parser)
        if not then_expr:
            return None

        _else = parser.consume()
        if _else.type != TokenType.ELSE:
            return None
        else_expr = any_expression_match(parser)
        if not else_expr:
            return None
        return IfExpression(if_expr=if_expr, then_expr=then_expr, else_expr=else_expr)
