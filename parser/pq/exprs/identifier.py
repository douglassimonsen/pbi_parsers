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
