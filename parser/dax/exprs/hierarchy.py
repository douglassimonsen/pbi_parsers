from typing import TYPE_CHECKING

from ..tokens import Token, TokenType
from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from ..parser import Parser


class HierarchyExpression(Expression):
    table: Token
    column: Token
    level: Token

    def __init__(self, table: Token, column: Token, level: Token):
        self.table = table
        self.column = column
        self.level = level

    def pprint(self) -> str:
        base = f"""
Hierarchy (
    {self.table.text}, 
    {self.column.text}
    {self.level.text}
)""".strip()
        return base

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "HierarchyExpression | None":
        table, column, period, level = (
            parser.consume(),
            parser.consume(),
            parser.consume(),
            parser.consume(),
        )
        if table.type not in (
            TokenType.SINGLE_QUOTED_IDENTIFIER,
            TokenType.UNQUOTED_IDENTIFIER,
        ):
            return None
        if column.type != TokenType.BRACKETED_IDENTIFIER:
            return None
        if period.type != TokenType.PERIOD:
            return None
        if level.type != TokenType.BRACKETED_IDENTIFIER:
            return None
        return HierarchyExpression(table=table, column=column, level=level)
