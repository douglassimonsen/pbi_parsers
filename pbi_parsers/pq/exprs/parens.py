from typing import TYPE_CHECKING

from pbi_parsers.pq.tokens import TokenType

from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from pbi_parsers.pq.parser import Parser


class ParenthesesExpression(Expression):
    inner_statement: Expression | None

    def __init__(self, inner_statement: Expression | None) -> None:
        self.inner_statement = inner_statement

    def pprint(self) -> str:
        return f"""
Parentheses (
    {self.inner_statement}
)""".strip()

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "ParenthesesExpression | None":
        from . import any_expression_match  # noqa: PLC0415

        if not cls.match_tokens(parser, [TokenType.LEFT_PAREN]):
            return None

        parser.consume()
        # when paired with an arrow expression, the value may not exist
        value = any_expression_match(parser)

        if parser.consume().tok_type != TokenType.RIGHT_PAREN:
            return None

        return ParenthesesExpression(inner_statement=value)
