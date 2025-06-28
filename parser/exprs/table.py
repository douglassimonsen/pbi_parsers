import textwrap
from typing import TYPE_CHECKING

from ..tokens import Token, TokenType
from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from ..parser import Parser


class TableExpression(Expression):
    name: Token

    def __init__(self, name: Token):
        self.name = name

    def pprint(self, depth: int = 0) -> str:
        base = f"""
Table (
    {self.name.text}
)""".strip()
        return textwrap.indent(base, " " * (depth * 4))

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "TableExpression | None":
        name = parser.consume()
        if name.type not in (
            TokenType.SINGLE_QUOTED_IDENTIFIER,
            TokenType.UNQUOTED_IDENTIFIER,
        ):
            return None
        return TableExpression(name=name)
