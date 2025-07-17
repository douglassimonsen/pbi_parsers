from typing import TYPE_CHECKING

from ..tokens import Token, TokenType
from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from ..parser import Parser


class ColumnExpression(Expression):
    name: Token

    def __init__(self, name: Token):
        self.name = name

    def pprint(self) -> str:
        base = f"Column ({self.name.text})"
        return base

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "ColumnExpression | None":
        if cls.match_tokens(parser, [TokenType.BRACKETED_IDENTIFIER]):
            name = parser.consume()
            return ColumnExpression(name=name)
