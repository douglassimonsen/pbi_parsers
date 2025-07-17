from typing import TYPE_CHECKING

from pbi_parsers.pq.tokens import Token, TokenType

from ._base import Expression
from ._utils import lexer_reset

if TYPE_CHECKING:
    from pbi_parsers.pq.parser import Parser


class ColumnExpression(Expression):
    name: Token

    def __init__(self, name: Token) -> None:
        self.name = name

    def pprint(self) -> str:
        return f"Column ({self.name.text})"

    @classmethod
    @lexer_reset
    def match(cls, parser: "Parser") -> "ColumnExpression | None":
        if cls.match_tokens(
            parser,
            [
                TokenType.LEFT_BRACKET,
                TokenType.UNQUOTED_IDENTIFIER,
                TokenType.RIGHT_BRACKET,
            ],
        ):
            _l_bracket, name, _r_bracket = (
                parser.consume(),
                parser.consume(),
                parser.consume(),
            )
            return ColumnExpression(name=name)
        return None

    def children(self) -> list[Expression]:  # noqa: PLR6301
        """Returns a list of child expressions."""
        return []
