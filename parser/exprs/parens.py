import textwrap
from typing import TYPE_CHECKING

from ..tokens import TokenType
from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from ..parser import Parser


class ParenthesesExpression(Expression):
    inner_statement: Expression

    def __init__(self, inner_statement: Expression):
        self.inner_statement = inner_statement

    def pprint(self, depth: int = 0) -> str:
        base = f"""
Parentheses (
    {self.inner_statement}
)""".strip()
        return textwrap.indent(base, " " * (depth * 4))

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "ParenthesesExpression | None":
        from . import any_expression_match

        if not cls.match_tokens(parser, [TokenType.LEFT_PAREN]):
            return None

        parser.consume()
        value = any_expression_match(parser)
        if value is None:
            raise ValueError(
                "ParenthesesExpression.match called without valid inner expression"
            )
        assert (
            parser.consume().type == TokenType.RIGHT_PAREN
        )  # Consume the right parenthesis
        return ParenthesesExpression(inner_statement=value)
