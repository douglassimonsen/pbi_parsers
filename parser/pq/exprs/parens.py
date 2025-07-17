from typing import TYPE_CHECKING

from ..tokens import TokenType
from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from ..parser import Parser


class ParenthesesExpression(Expression):
    inner_statement: Expression | None

    def __init__(self, inner_statement: Expression):
        self.inner_statement = inner_statement

    def pprint(self) -> str:
        base = f"""
Parentheses (
    {self.inner_statement}
)""".strip()
        return base

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "ParenthesesExpression | None":
        from . import any_expression_match

        if not cls.match_tokens(parser, [TokenType.LEFT_PAREN]):
            return None

        parser.consume()
        # when paired with an arrow expression, the value may not exist
        value = any_expression_match(parser)
        if parser.consume().type != TokenType.RIGHT_PAREN:
            return None
        return ParenthesesExpression(inner_statement=value)
