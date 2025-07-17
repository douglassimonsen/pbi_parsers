import textwrap
from typing import TYPE_CHECKING

from pbi_parsers.pq.tokens import TokenType

from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from pbi_parsers.pq.parser import Parser


class MetaExpression(Expression):
    left_term: Expression
    right_term: Expression

    def __init__(self, left_term: Expression, right_term: Expression) -> None:
        self.left_term = left_term
        self.right_term = right_term

    def pprint(self) -> str:
        left_term = textwrap.indent(self.left_term.pprint(), " " * 10)[10:]
        right_term = textwrap.indent(self.right_term.pprint(), " " * 10)[10:]
        return f"""
Meta (
    left: {left_term},
    right: {right_term},
)""".strip()

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "MetaExpression | None":
        from . import EXPRESSION_HIERARCHY, any_expression_match  # noqa: PLC0415

        skip_index = EXPRESSION_HIERARCHY.index(MetaExpression)
        left_term = any_expression_match(parser=parser, skip_first=skip_index + 1)
        if left_term is None:
            return None

        meta = parser.consume()
        if meta.tok_type != TokenType.META:
            return None

        right_term: Expression | None = any_expression_match(
            parser,
        )  # this expression can recurse
        if not right_term:
            return None

        return MetaExpression(left_term=left_term, right_term=right_term)

    def children(self) -> list[Expression]:
        """Returns a list of child expressions."""
        return [self.left_term, self.right_term]
