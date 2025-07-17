from typing import TYPE_CHECKING

from pbi_parsers.pq.tokens import Token, TokenType

from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from pbi_parsers.pq.parser import Parser


class LiteralStringExpression(Expression):
    value: Token

    def __init__(self, value: Token) -> None:
        self.value = value

    def pprint(self) -> str:
        return f"String ({self.value.text})"

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "LiteralStringExpression | None":
        if cls.match_tokens(parser, [TokenType.STRING_LITERAL]):
            value = parser.consume()
            return LiteralStringExpression(value=value)
        return None

    def children(self) -> list[Expression]:  # noqa: PLR6301
        """Returns a list of child expressions."""
        return []
