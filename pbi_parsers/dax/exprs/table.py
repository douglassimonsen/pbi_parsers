from typing import TYPE_CHECKING

from pbi_parsers.dax.tokens import Token, TokenType

from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from pbi_parsers.dax.parser import Parser


class TableExpression(Expression):
    name: Token

    def __init__(self, name: Token) -> None:
        self.name = name

    def pprint(self) -> str:
        return f"""
Table (
    {self.name.text}
)""".strip()

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "TableExpression | None":
        name = parser.consume()
        if name.tok_type not in {
            TokenType.SINGLE_QUOTED_IDENTIFIER,
            TokenType.UNQUOTED_IDENTIFIER,
        }:
            return None
        return TableExpression(name=name)
