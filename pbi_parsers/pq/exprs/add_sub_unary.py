import textwrap
from typing import TYPE_CHECKING

from pbi_parsers.pq.tokens import Token, TokenType

from ._base import Expression
from ._utils import lexer_reset

if TYPE_CHECKING:
    from pbi_parsers.pq.parser import Parser


class AddSubUnaryExpression(Expression):
    """Represents an addition or subtraction expression."""

    operator: Token
    number: Expression

    def __init__(self, operator: Token, number: Expression) -> None:
        self.operator = operator
        self.number = number

    @classmethod
    @lexer_reset
    def match(cls, parser: "Parser") -> "AddSubUnaryExpression | None":
        from . import EXPRESSION_HIERARCHY, any_expression_match  # noqa: PLC0415

        skip_index = EXPRESSION_HIERARCHY.index(
            AddSubUnaryExpression,
        )  # intentionally inclusive of self to allow +-++- chains

        operator = parser.consume()

        if operator.tok_type not in {TokenType.PLUS_SIGN, TokenType.MINUS_SIGN}:
            return None

        # Handle chained +-++-+ prefixes
        number: Expression | None = any_expression_match(
            parser=parser,
            skip_first=skip_index,
        )
        if number is None:
            msg = f"Expected a number after operator {operator.text}, found: {parser.peek()}"
            raise ValueError(msg)
        return AddSubUnaryExpression(operator=operator, number=number)

    def pprint(self) -> str:
        number = textwrap.indent(self.number.pprint(), " " * 12).lstrip()
        return f"""
Number (
    sign: {self.operator.text},
    number: {number},
)""".strip()

    def children(self) -> list[Expression]:
        """Returns a list of child expressions."""
        return [self.number]
