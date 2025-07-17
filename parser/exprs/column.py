import textwrap

from git import TYPE_CHECKING

from ..tokens import Token, TokenType
from ._base import Expression

if TYPE_CHECKING:
    from ..parser import Parser


class ColumnExpression(Expression):
    table: Token
    column: Token

    def __init__(self, table: Token, column: Token):
        self.table = table
        self.column = column

    def pprint(self, depth: int = 0) -> str:
        base = f"""
Column (
    {self.table.text}, 
    {self.column.text}
)""".strip()
        return textwrap.indent(base, " " * (depth * 4))

    @classmethod
    def match(cls, parser: "Parser") -> "ColumnExpression | None":
        if cls.match_tokens(
            parser, [TokenType.SINGLE_QUOTED_IDENTIFIER, TokenType.BRACKETED_IDENTIFIER]
        ):
            table, column = parser.consume(), parser.consume()
            return ColumnExpression(table=table, column=column)
