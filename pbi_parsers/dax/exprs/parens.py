from typing import TYPE_CHECKING

from pbi_parsers.dax.tokens import Token, TokenType

from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from pbi_parsers.dax.parser import Parser


class ParenthesesExpression(Expression):
    inner_statement: Expression
    parens: tuple[Token, Token]

    def __init__(self, inner_statement: Expression, parens: tuple[Token, Token]) -> None:
        self.inner_statement = inner_statement
        self.parens = parens

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

        left_paren = parser.consume()
        value = any_expression_match(parser)
        if value is None:
            msg = "ParenthesesExpression.match called without valid inner expression"
            raise ValueError(msg)
        right_paren = parser.consume()
        assert right_paren.tok_type == TokenType.RIGHT_PAREN  # Consume the right parenthesis
        return ParenthesesExpression(inner_statement=value, parens=(left_paren, right_paren))

    def children(self) -> list[Expression]:
        """Returns a list of child expressions."""
        return [self.inner_statement]

    def position(self) -> tuple[int, int]:
        """Returns the position of the expression."""
        return self.parens[0].text_slice.start, self.parens[1].text_slice.end

    def full_text(self) -> str:
        """Returns the full text of the expression."""
        return self.parens[0].text_slice.full_text
