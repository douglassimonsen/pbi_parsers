import textwrap
from typing import TYPE_CHECKING

from ..tokens import TokenType
from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from ..parser import Parser


class NegationExpression(Expression):
    """
    Represents a negation expression.
    """

    number: Expression

    def __init__(self, number: Expression):
        self.number = number

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "NegationExpression | None":
        from . import EXPRESSION_HIERARCHY, any_expression_match

        skip_index = EXPRESSION_HIERARCHY.index(
            NegationExpression
        )  # intentionally inclusive of self to allow +-++- chains

        if parser.consume().type != TokenType.EXCLAMATION_POINT:
            return None

        # Handle chained !!! prefixes
        number: Expression | None = any_expression_match(
            parser=parser, skip_first=skip_index
        )
        if number is None:
            raise ValueError(
                f'Expected a right term after negation "!", found: {parser.peek()}'
            )
        return NegationExpression(number=number)

    def pprint(self) -> str:
        number = textwrap.indent(self.number.pprint(), " " * 12).lstrip()
        return f"""
Negation (
    number: {number},
)""".strip()
