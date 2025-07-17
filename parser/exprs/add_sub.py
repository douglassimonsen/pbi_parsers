from functools import partial
from typing import TYPE_CHECKING

from ..tokens import Token, TokenType
from ._base import Expression
from ._utils import or_match
from .column import ColumnExpression
from .div_mul import DivMulExpression
from .function import FunctionExpression
from .literal_number import LiteralNumberExpression
from .literal_string import LiteralStringExpression
from .measure import MeasureExpression

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
    def match(cls, parser: "Parser") -> "AddSubExpression | None":
        left_term = add_sub_match(parser=parser)
        if not left_term:
            return None
        if not cls.match_tokens(parser, [TokenType.OPERATOR]):
            return None
        if parser.peek().text not in ("+", "-"):
            return None
        operator = parser.pop()
        right_term = add_sub_match(parser=parser)
        if right_term is None:
            raise ValueError(
                f"Expected a right term after operator {operator.text}, found: {parser.peek()}"
            )
        return AddSubExpression(operator=operator, left=left_term, right=right_term)

    def __repr__(self, depth: int = 0) -> str:
        if self.operator.text == "+":
            op_str = "Add"
        else:
            op_str = "Sub"
        left_str = self.left.pprint(depth + 1)
        right_str = self.right.pprint(depth + 1)
        return f"""
{op_str} (
    operator: {self.operator.text},
    left: {left_str},
    right: {right_str}
)"""
