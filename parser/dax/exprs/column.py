from typing import TYPE_CHECKING

from ..tokens import Token, TokenType
from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from ..parser import Parser


class ColumnExpression(Expression):
    table: Token
    column: Token

    def __init__(self, table: Token, column: Token):
        self.table = table
        self.column = column

    def pprint(self) -> str:
        base = f"""
Column (
    {self.table.text}, 
    {self.column.text}
)""".strip()
        return base

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "ColumnExpression | None":
        table, column = parser.consume(), parser.consume()
        if table.type not in (
            TokenType.SINGLE_QUOTED_IDENTIFIER,
            TokenType.UNQUOTED_IDENTIFIER,
        ):
            return None
        if column.type != TokenType.BRACKETED_IDENTIFIER:
            return None
        return ColumnExpression(table=table, column=column)
