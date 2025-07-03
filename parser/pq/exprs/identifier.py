from typing import TYPE_CHECKING

from ..tokens import TEXT_TOKENS, Token, TokenType
from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from ..parser import Parser


class IdentifierExpression(Expression):
    name_parts: list[Token]

    def __init__(self, name_parts: list[Token]):
        self.name_parts = name_parts

    def pprint(self) -> str:
        name = ".".join(part.text for part in self.name_parts)
        base = f"Identifier ({name})"
        return base

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "IdentifierExpression | None":
        name_parts = [parser.consume()]
        if (
            name_parts[0].type
            not in (
                TokenType.QUOTED_IDENTIFER,
                TokenType.UNQUOTED_IDENTIFIER,
                *TEXT_TOKENS,
            )
        ):  # TEXT_TOKENS are used to allow keywords to be used as identifiers. This requires identifiers to be matched after keywords.
            return None

        while parser.peek().type == TokenType.PERIOD:
            _period, name = parser.consume(), parser.consume()
            if name.type != TokenType.UNQUOTED_IDENTIFIER:
                return None
            name_parts.append(name)

        return IdentifierExpression(name_parts=name_parts)


class BracketedIdentifierExpression(Expression):
    name: list[Token]

    def __init__(self, name_parts: list[Token]):
        self.name_parts = name_parts

    def pprint(self) -> str:
        base = f"""
Bracketed Identifier ({' '.join(part.text for part in self.name_parts)})""".strip()
        return base

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "BracketedIdentifierExpression | None":
        _left_bracket = parser.consume()
        if _left_bracket.type != TokenType.LEFT_BRACKET:
            return None
        name_parts = []
        while parser.peek().type in (
            TokenType.UNQUOTED_IDENTIFIER,
            *TEXT_TOKENS,
        ):  # there are cases where keywords can be used as identifiers
            name = parser.consume()
            name_parts.append(name)
        _right_bracket = parser.consume()
        if _right_bracket.type != TokenType.RIGHT_BRACKET:
            return None
        return BracketedIdentifierExpression(name_parts=name_parts)
