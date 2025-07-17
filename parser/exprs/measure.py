import textwrap
from typing import TYPE_CHECKING
from ..tokens import Token, TokenType
from ._base import Expression
if TYPE_CHECKING:
    from ..parser import Parser


class MeasureExpression(Expression):
    name: Token

    def __init__(self, name: Token):
        self.name = name

    def pprint(self, depth: int = 0) -> str:
        base = f"Measure ({self.name.text})"
        return textwrap.indent(base, " " * (depth * 4))

    @classmethod
    def match(cls, parser: "Parser") -> "MeasureExpression | None":
        if cls.match_tokens(parser, [TokenType.BRACKETED_IDENTIFIER]):
            name = parser.pop()
            return MeasureExpression(name=name)
