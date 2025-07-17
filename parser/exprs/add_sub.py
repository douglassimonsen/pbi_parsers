import textwrap
from functools import partial
from typing import TYPE_CHECKING

from ..tokens import Token, TokenType
from ._base import Expression
from ._utils import or_match, scanner_reset
from .column import ColumnExpression
from .div_mul import DivMulExpression
from .function import FunctionExpression
from .literal_number import LiteralNumberExpression
from .literal_string import LiteralStringExpression
from .measure import MeasureExpression
from .parens import ParenthesesExpression

if TYPE_CHECKING:
    from ..parser import Parser

add_sub_match = partial(
    or_match,
    exprs=(
        DivMulExpression,
        ColumnExpression,
        MeasureExpression,
        FunctionExpression,
        LiteralStringExpression,
        LiteralNumberExpression,
        ParenthesesExpression,
    ),
)


class AddSubExpression(Expression):
    """
    Represents an addition or subtraction expression.
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
    def match(cls, parser: "Parser") -> "AddSubExpression | None":
        left_term = add_sub_match(parser=parser)
        operator = parser.consume()

        if not left_term:
            return None
        if operator.type != TokenType.OPERATOR or operator.text not in ("+", "-"):
            return None

        right_term = add_sub_match(parser=parser)
        if right_term is None:
            raise ValueError(
                f"Expected a right term after operator {operator.text}, found: {parser.peek()}"
            )
        return AddSubExpression(operator=operator, left=left_term, right=right_term)

    def pprint(self) -> str:
        if self.operator.text == "+":
            op_str = "Add"
        else:
            op_str = "Sub"
        left_str = textwrap.indent(self.left.pprint(), " " * 10).lstrip()
        right_str = textwrap.indent(self.right.pprint(), " " * 10).lstrip()
        return f"""
{op_str} (
    operator: {self.operator.text},
    left: {left_str},
    right: {right_str}
)""".strip()
