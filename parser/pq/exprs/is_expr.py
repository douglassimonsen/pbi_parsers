import textwrap
from typing import TYPE_CHECKING

from ..tokens import TokenType
from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from ..parser import Parser


class IsExpression(Expression):
    """
    Represents an multiplication or division expression.
    """

    left: Expression
    right: Expression

    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "IsExpression | None":
        from . import EXPRESSION_HIERARCHY, any_expression_match

        skip_index = EXPRESSION_HIERARCHY.index(IsExpression)

        left_term = any_expression_match(parser=parser, skip_first=skip_index + 1)

        if not left_term:
            return None
        if parser.consume().type != TokenType.IS:
            return None

        right_term = any_expression_match(parser=parser, skip_first=skip_index)
        if right_term is None:
            raise ValueError(
                f'Expected a right term after operator "is", found: {parser.peek()}'
            )
        return IsExpression(left=left_term, right=right_term)

    def pprint(self) -> str:
        left_str = textwrap.indent(self.left.pprint(), " " * 10)[10:]
        right_str = textwrap.indent(self.right.pprint(), " " * 10)[10:]
        return f"""
Is (
    left: {left_str},
    right: {right_str}
)""".strip()
