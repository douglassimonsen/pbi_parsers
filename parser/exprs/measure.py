import textwrap
from typing import TYPE_CHECKING

from ..tokens import Token, TokenType
from ._base import Expression
from ._utils import scanner_reset

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
    @scanner_reset
    def match(cls, parser: "Parser") -> "MeasureExpression | None":
        if cls.match_tokens(parser, [TokenType.BRACKETED_IDENTIFIER]):
            name = parser.consume()
            return MeasureExpression(name=name)
