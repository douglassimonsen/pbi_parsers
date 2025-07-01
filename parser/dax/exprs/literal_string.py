from typing import TYPE_CHECKING

from ..tokens import Token, TokenType
from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from ..parser import Parser


class LiteralStringExpression(Expression):
    value: Token

    def __init__(self, value: Token):
        self.value = value

    def pprint(self) -> str:
        base = f"String ({self.value.text})"
        return base

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "LiteralStringExpression | None":
        if cls.match_tokens(parser, [TokenType.STRING_LITERAL]):
            value = parser.consume()
            return LiteralStringExpression(value=value)
