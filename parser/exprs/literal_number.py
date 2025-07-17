import textwrap
from typing import TYPE_CHECKING

from ..tokens import Token, TokenType
from ._base import Expression

if TYPE_CHECKING:
    from ..parser import Parser


class LiteralNumberExpression(Expression):
    value: Token

    def __init__(self, value: Token):
        self.value = value

    def pprint(self, depth: int = 0) -> str:
        base = f"Number ({self.value.text})"
        return textwrap.indent(base, " " * (depth * 4))

    @classmethod
    def match(cls, parser: "Parser") -> "LiteralNumberExpression | None":
        if cls.match_tokens(parser, [TokenType.NUMBER_LITERAL]):
            value = parser.pop()
            return LiteralNumberExpression(value=value)
