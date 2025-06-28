import textwrap
from functools import partial
from typing import TYPE_CHECKING

from ..tokens import Token, TokenType
from ._base import Expression
from ._utils import or_match, scanner_reset
from .add_sub import AddSubExpression
from .column import ColumnExpression
from .div_mul import DivMulExpression
from .function import FunctionExpression
from .literal_number import LiteralNumberExpression
from .literal_string import LiteralStringExpression
from .measure import MeasureExpression
from .parens import ParenthesesExpression

if TYPE_CHECKING:
    from ..parser import Parser

bool_match = partial(
    or_match,
    exprs=(
        AddSubExpression,
        DivMulExpression,
        ColumnExpression,
        MeasureExpression,
        FunctionExpression,
        LiteralStringExpression,
        LiteralNumberExpression,
        ParenthesesExpression,
    ),
)


class BoolExpression(Expression):
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
    def match(cls, parser: "Parser") -> "BoolExpression | None":
        left_term = bool_match(parser=parser)
        if not left_term:
            return None
        if not cls.match_tokens(parser, [TokenType.EQUAL_SIGN]):
            return None
        if parser.peek().text != "=":
            return None
        operator = parser.consume()
        right_term = bool_match(parser=parser)
        if right_term is None:
            raise ValueError(
                f"Expected a right term after operator {operator.text}, found: {parser.peek()}"
            )
        return BoolExpression(operator=operator, left=left_term, right=right_term)

    def pprint(self, depth: int = 0) -> str:
        left_str = textwrap.indent(self.left.pprint(), " " * 10)[10:]
        right_str = textwrap.indent(self.right.pprint(), " " * 10)[10:]
        return f"""
Bool (
    operator: {self.operator.text},
    left: {left_str},
    right: {right_str}
)""".strip()
