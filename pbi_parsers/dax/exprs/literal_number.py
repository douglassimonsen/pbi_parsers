from typing import TYPE_CHECKING

from pbi_parsers.dax.tokens import Token, TokenType

from ._base import Expression
from ._utils import lexer_reset

if TYPE_CHECKING:
    from pbi_parsers.dax.parser import Parser


class LiteralNumberExpression(Expression):
    """Represents a literal number in DAX.

    Examples:
        42
        3.14
        -1000

    """

    value: Token

    def __init__(self, value: Token) -> None:
        self.value = value

    def pprint(self) -> str:
        return f"Number ({self.value.text})"

    @classmethod
    @lexer_reset
    def match(cls, parser: "Parser") -> "LiteralNumberExpression | None":
        if cls.match_tokens(parser, [TokenType.NUMBER_LITERAL]):
            value = parser.consume()
            return LiteralNumberExpression(value=value)
        return None

    def children(self) -> list[Expression]:  # noqa: PLR6301
        """Returns a list of child expressions."""
        return []

    def position(self) -> tuple[int, int]:
        return self.value.text_slice.start, self.value.text_slice.end

    def full_text(self) -> str:
        return self.value.text_slice.full_text
