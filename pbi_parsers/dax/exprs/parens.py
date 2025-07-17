from typing import TYPE_CHECKING

from pbi_parsers.dax.tokens import TokenType

from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from pbi_parsers.dax.parser import Parser


class ParenthesesExpression(Expression):
    inner_statement: Expression

    def __init__(self, inner_statement: Expression) -> None:
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
        value = any_expression_match(parser)
        if value is None:
            msg = "ParenthesesExpression.match called without valid inner expression"
            raise ValueError(msg)
        assert parser.consume().tok_type == TokenType.RIGHT_PAREN  # Consume the right parenthesis
        return ParenthesesExpression(inner_statement=value)

    def children(self) -> list[Expression]:
        """Returns a list of child expressions."""
        return [self.inner_statement]
