import textwrap
from typing import TYPE_CHECKING

from ..tokens import Token, TokenType
from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from ..parser import Parser


class LogicalExpression(Expression):
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
    def match(cls, parser: "Parser") -> "LogicalExpression | None":
        from . import EXPRESSION_HIERARCHY, any_expression_match

        skip_index = EXPRESSION_HIERARCHY.index(LogicalExpression)

        left_term = any_expression_match(parser=parser, skip_first=skip_index + 1)
        operator = parser.consume()

        if not left_term:
            return None
        if operator.type not in (
            TokenType.DOUBLE_PIPE_OPERATOR,
            TokenType.DOUBLE_AMPERSAND_OPERATOR,
        ):
            return None

        right_term: Expression | None = any_expression_match(
            parser=parser, skip_first=skip_index
        )
        if right_term is None:
            raise ValueError(
                f"Expected a right term after operator {operator.text}, found: {parser.peek()}"
            )
        return LogicalExpression(operator=operator, left=left_term, right=right_term)

    def pprint(self) -> str:
        if self.operator.text == "&&":
            op_str = "And"
        else:
            op_str = "Or"
        left_str = textwrap.indent(self.left.pprint(), " " * 10).lstrip()
        right_str = textwrap.indent(self.right.pprint(), " " * 10).lstrip()
        return f"""
{op_str} (
    operator: {self.operator.text},
    left: {left_str},
    right: {right_str}
)""".strip()
