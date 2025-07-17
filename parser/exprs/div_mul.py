import textwrap
from functools import partial
from typing import TYPE_CHECKING

from ..tokens import Token, TokenType
from ._base import Expression
from ._utils import or_match, scanner_reset
from .column import ColumnExpression
from .function import FunctionExpression
from .literal_number import LiteralNumberExpression
from .literal_string import LiteralStringExpression
from .measure import MeasureExpression
from .parens import ParenthesesExpression

if TYPE_CHECKING:
    from ..parser import Parser
div_mul_match = partial(
    or_match,
    exprs=(
        ColumnExpression,
        MeasureExpression,
        FunctionExpression,
        LiteralStringExpression,
        LiteralNumberExpression,
        ParenthesesExpression,
    ),
)


class DivMulExpression(Expression):
    """
    Represents an multiplication or division expression.
    """

    operator: Token
    left: Expression
    right: Expression

    def __init__(self, operator: Token, left: Expression, right: Expression):
        self.operator = operator
        self.left = left
        self.right = right

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "DivMulExpression | None":
        left_term = div_mul_match(parser=parser)
        if not left_term:
            return None
        if not cls.match_tokens(parser, [TokenType.OPERATOR]):
            return None
        if parser.peek().text not in ("*", "/"):
            return None
        operator = parser.consume()
        right_term = div_mul_match(parser=parser)
        if right_term is None:
            raise ValueError(
                f"Expected a right term after operator {operator.text}, found: {parser.peek()}"
            )
        return DivMulExpression(operator=operator, left=left_term, right=right_term)

    def pprint(self, depth: int = 0) -> str:
        if self.operator.text == "*":
            op_str = "Mul"
        else:
            op_str = "Div"
        left_str = textwrap.indent(self.left.pprint(), " " * 10)[10:]
        right_str = textwrap.indent(self.right.pprint(), " " * 10)[10:]
        return f"""
{op_str} (
    operator: {self.operator.text},
    left: {left_str},
    right: {right_str}
)""".strip()
