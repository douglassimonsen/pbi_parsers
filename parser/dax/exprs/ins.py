import textwrap
from typing import TYPE_CHECKING

from ..tokens import TokenType
from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from ..parser import Parser


class InExpression(Expression):
    """
    Represents an multiplication or division expression.
    """

    value: Expression
    array: Expression

    def __init__(self, value: Expression, array: Expression):
        self.value = value
        self.array = array

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "InExpression | None":
        from . import EXPRESSION_HIERARCHY, any_expression_match

        skip_index = EXPRESSION_HIERARCHY.index(InExpression)

        left_term = any_expression_match(parser=parser, skip_first=skip_index + 1)
        operator = parser.consume()

        if not left_term:
            return None
        if operator.type != TokenType.IN:
            return None

        right_term = any_expression_match(parser=parser, skip_first=skip_index)
        if right_term is None:
            raise ValueError(
                f"Expected a right term after operator {operator.text}, found: {parser.peek()}"
            )
        return InExpression(value=left_term, array=right_term)

    def pprint(self) -> str:
        value_str = textwrap.indent(self.value.pprint(), " " * 11)[11:]
        array_str = textwrap.indent(self.array.pprint(), " " * 11)[11:]
        return f"""
In (
    value: {value_str},
    array: {array_str}
)""".strip()
