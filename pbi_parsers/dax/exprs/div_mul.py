import textwrap
from typing import TYPE_CHECKING

from pbi_parsers.dax.tokens import Token, TokenType

from ._base import Expression
from ._utils import lexer_reset

if TYPE_CHECKING:
    from pbi_parsers.dax.parser import Parser


class DivMulExpression(Expression):
    """Represents an multiplication or division expression."""

    operator: Token
    left: Expression
    right: Expression

    def __init__(self, operator: Token, left: Expression, right: Expression) -> None:
        self.operator = operator
        self.left = left
        self.right = right

    @classmethod
    @lexer_reset
    def match(cls, parser: "Parser") -> "DivMulExpression | None":
        from . import EXPRESSION_HIERARCHY, any_expression_match  # noqa: PLC0415

        skip_index = EXPRESSION_HIERARCHY.index(DivMulExpression)

        left_term = any_expression_match(parser=parser, skip_first=skip_index + 1)
        operator = parser.consume()

        if not left_term:
            return None
        if operator.tok_type not in {TokenType.MULTIPLY_SIGN, TokenType.DIVIDE_SIGN}:
            return None

        right_term = any_expression_match(parser=parser, skip_first=skip_index)
        if right_term is None:
            msg = f"Expected a right term after operator {operator.text}, found: {parser.peek()}"
            raise ValueError(msg)
        return DivMulExpression(operator=operator, left=left_term, right=right_term)

    def pprint(self) -> str:
        op_str = {
            TokenType.MULTIPLY_SIGN: "Mul",
            TokenType.DIVIDE_SIGN: "Div",
        }[self.operator.tok_type]
        left_str = textwrap.indent(self.left.pprint(), " " * 10)[10:]
        right_str = textwrap.indent(self.right.pprint(), " " * 10)[10:]
        return f"""
{op_str} (
    left: {left_str},
    right: {right_str}
)""".strip()

    def children(self) -> list[Expression]:
        """Returns a list of child expressions."""
        return [self.left, self.right]

    def position(self) -> tuple[int, int]:
        return self.left.position()[0], self.right.position()[1]

    def full_text(self) -> str:
        return self.operator.text_slice.full_text
