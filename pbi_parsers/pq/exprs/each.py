import textwrap
from typing import TYPE_CHECKING

from pbi_parsers.pq.tokens import TokenType

from ._base import Expression
from ._utils import lexer_reset

if TYPE_CHECKING:
    from pbi_parsers.pq.parser import Parser


class EachExpression(Expression):
    each_expr: Expression

    def __init__(self, each_expr: Expression) -> None:
        self.each_expr = each_expr

    def pprint(self) -> str:
        each_expr = textwrap.indent(self.each_expr.pprint(), " " * 10)[10:]
        return f"""
Each (
    each: {each_expr},
)""".strip()

    @classmethod
    @lexer_reset
    def match(cls, parser: "Parser") -> "EachExpression | None":
        from . import any_expression_match  # noqa: PLC0415

        each = parser.consume()
        if each.tok_type != TokenType.EACH:
            return None
        each_expr: Expression | None = any_expression_match(parser)
        if not each_expr:
            return None
        return EachExpression(each_expr=each_expr)

    def children(self) -> list[Expression]:
        """Returns a list of child expressions."""
        return [self.each_expr]
