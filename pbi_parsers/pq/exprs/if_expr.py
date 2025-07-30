import textwrap
from typing import TYPE_CHECKING

from pbi_parsers.pq.tokens import TokenType

from ._base import Expression
from ._utils import lexer_reset

if TYPE_CHECKING:
    from pbi_parsers.pq.parser import Parser


class IfExpression(Expression):
    if_expr: Expression
    then_expr: Expression
    else_expr: Expression

    def __init__(
        self,
        if_expr: Expression,
        then_expr: Expression,
        else_expr: Expression,
    ) -> None:
        self.if_expr = if_expr
        self.then_expr = then_expr
        self.else_expr = else_expr

    def pprint(self) -> str:
        if_expr = textwrap.indent(self.if_expr.pprint(), " " * 10)[10:]
        then_expr = textwrap.indent(self.then_expr.pprint(), " " * 10)[10:]
        else_expr = textwrap.indent(self.else_expr.pprint(), " " * 10)[10:]
        return f"""
If (
    if: {if_expr},
    then: {then_expr},
    else: {else_expr}
)""".strip()

    @classmethod
    @lexer_reset
    def match(cls, parser: "Parser") -> "IfExpression | None":  # noqa: PLR0911
        from . import any_expression_match  # noqa: PLC0415

        if_ = parser.consume()
        if if_.tok_type != TokenType.IF:
            return None
        if_expr: Expression | None = any_expression_match(
            parser,
        )  # this expression can recurse
        if not if_expr:
            return None

        then = parser.consume()
        if then.tok_type != TokenType.THEN:
            return None
        then_expr = any_expression_match(parser)
        if not then_expr:
            return None

        else_ = parser.consume()
        if else_.tok_type != TokenType.ELSE:
            return None
        else_expr = any_expression_match(parser)
        if not else_expr:
            return None
        return IfExpression(if_expr=if_expr, then_expr=then_expr, else_expr=else_expr)

    def children(self) -> list[Expression]:
        """Returns a list of child expressions."""
        return [self.if_expr, self.then_expr, self.else_expr]
