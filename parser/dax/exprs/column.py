from typing import TYPE_CHECKING

from parser.dax.tokens import Token, TokenType

from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from parser.dax.parser import Parser


class ColumnExpression(Expression):
    table: Token
    column: Token

    def __init__(self, table: Token, column: Token) -> None:
        self.table = table
        self.column = column

    def pprint(self) -> str:
        return f"""
Column (
    {self.table.text},
    {self.column.text}
)""".strip()

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "ColumnExpression | None":
        table, column = parser.consume(), parser.consume()
        if table.tok_type not in {
            TokenType.SINGLE_QUOTED_IDENTIFIER,
            TokenType.UNQUOTED_IDENTIFIER,
        }:
            return None
        if column.tok_type != TokenType.BRACKETED_IDENTIFIER:
            return None
        return ColumnExpression(table=table, column=column)
