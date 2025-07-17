import textwrap
from typing import TYPE_CHECKING

from pbi_parsers.dax.tokens import TokenType

from ._base import Expression
from ._utils import lexer_reset

if TYPE_CHECKING:
    from pbi_parsers.dax.parser import Parser


class InExpression(Expression):
    """Represents an multiplication or division expression."""

    value: Expression
    array: Expression

    def __init__(self, value: Expression, array: Expression) -> None:
        self.value = value
        self.array = array

    @classmethod
    @lexer_reset
    def match(cls, parser: "Parser") -> "InExpression | None":
        from . import EXPRESSION_HIERARCHY, any_expression_match  # noqa: PLC0415

        skip_index = EXPRESSION_HIERARCHY.index(InExpression)

        left_term = any_expression_match(parser=parser, skip_first=skip_index + 1)
        operator = parser.consume()

        if not left_term:
            return None
        if operator.tok_type != TokenType.IN:
            return None

        right_term = any_expression_match(parser=parser, skip_first=skip_index)
        if right_term is None:
            msg = f"Expected a right term after operator {operator.text}, found: {parser.peek()}"
            raise ValueError(msg)
        return InExpression(value=left_term, array=right_term)

    def pprint(self) -> str:
        value_str = textwrap.indent(self.value.pprint(), " " * 11)[11:]
        array_str = textwrap.indent(self.array.pprint(), " " * 11)[11:]
        return f"""
In (
    value: {value_str},
    array: {array_str}
)""".strip()

    def children(self) -> list[Expression]:
        """Returns a list of child expressions."""
        return [self.value, self.array]

    def position(self) -> tuple[int, int]:
        return self.value.position()[0], self.array.position()[1]

    def full_text(self) -> str:
        return self.value.full_text()
