from typing import TYPE_CHECKING

from ..tokens import Token, TokenType
from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from ..parser import Parser


class IdentifierExpression(Expression):
    name: Token

    def __init__(self, name: Token):
        self.name = name

    def pprint(self) -> str:
        base = f"""
Identifier ({self.name.text})""".strip()
        return base

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "IdentifierExpression | None":
        name = parser.consume()
        if name.type not in (
            TokenType.QUOTED_IDENTIFER,
            TokenType.UNQUOTED_IDENTIFIER,
        ):
            return None
        return IdentifierExpression(name=name)


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
        while parser.peek().type == TokenType.UNQUOTED_IDENTIFIER:
            name = parser.consume()
            name_parts.append(name)
        _right_bracket = parser.consume()
        if _right_bracket.type != TokenType.RIGHT_BRACKET:
            return None
        return BracketedIdentifierExpression(name_parts=name_parts)
