from typing import TYPE_CHECKING

from ..tokens import Token, TokenType
from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from ..parser import Parser


class KeywordExpression(Expression):
    name: Token

    def __init__(self, name: Token):
        self.name = name

    def pprint(self) -> str:
        base = f"""
Keyword ({self.name.text})""".strip()
        return base

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "KeywordExpression | None":
        name = parser.consume()
        if name.type != TokenType.KEYWORD:
            return None
        return KeywordExpression(name=name)
