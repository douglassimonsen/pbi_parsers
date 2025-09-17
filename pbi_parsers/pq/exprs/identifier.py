from typing import TYPE_CHECKING

from pbi_parsers.pq.tokens import TEXT_TOKENS, Token, TokenType

from ._base import Expression
from ._utils import lexer_reset

if TYPE_CHECKING:
    from pbi_parsers.pq.parser import Parser

NAME_PARTS = (
    TokenType.QUOTED_IDENTIFER,
    TokenType.UNQUOTED_IDENTIFIER,
    TokenType.HASH_IDENTIFIER,
    *TEXT_TOKENS,
)


class IdentifierExpression(Expression):
    name_parts: list[Token]

    def __init__(self, name_parts: list[Token]) -> None:
        self.name_parts = name_parts

    def name(self) -> str:
        """Returns the full identifier name as a string."""
        return ".".join(part.text for part in self.name_parts)

    def pprint(self) -> str:
        return f"Identifier ({self.name()})"

    @classmethod
    @lexer_reset
    def match(cls, parser: "Parser") -> "IdentifierExpression | None":
        name_parts = [parser.consume()]
        if (
            name_parts[0].tok_type not in NAME_PARTS
        ):  # TEXT_TOKENS are used to allow keywords to be used as identifiers.
            # This requires identifiers to be matched after keywords.
            return None

        while parser.peek().tok_type == TokenType.PERIOD:
            _period, name = parser.consume(), parser.consume()
            if name.tok_type not in NAME_PARTS:
                return None
            name_parts.append(name)

        return IdentifierExpression(name_parts=name_parts)

    def children(self) -> list[Expression]:  # noqa: PLR6301
        return []


class BracketedIdentifierExpression(Expression):
    name: list[Token]

    def __init__(self, name_parts: list[Token]) -> None:
        self.name_parts = name_parts

    def pprint(self) -> str:
        return f"""
Bracketed Identifier ({" ".join(part.text for part in self.name_parts)})""".strip()

    @classmethod
    @lexer_reset
    def match(cls, parser: "Parser") -> "BracketedIdentifierExpression | None":
        left_bracket = parser.consume()
        if left_bracket.tok_type != TokenType.LEFT_BRACKET:
            return None
        name_parts = []
        while parser.peek().tok_type in {
            *NAME_PARTS,
            TokenType.PERIOD,
        }:  # there are cases where keywords can be used as identifiers
            name = parser.consume()
            name_parts.append(name)
        right_bracket = parser.consume()
        if right_bracket.tok_type != TokenType.RIGHT_BRACKET:
            return None
        return BracketedIdentifierExpression(name_parts=name_parts)

    def children(self) -> list[Expression]:  # noqa: PLR6301
        return []
