from typing import TYPE_CHECKING

from pbi_parsers.dax.tokens import Token, TokenType

from ._base import Expression
from ._utils import lexer_reset

if TYPE_CHECKING:
    from pbi_parsers.dax.parser import Parser


class HierarchyExpression(Expression):
    """Represents a hierarchy in DAX.

    Examples:
        Table[Column].[Level]
        'Table Name'[Column Name].[Level Name]

    """

    table: Token
    column: Token
    level: Token

    def __init__(self, table: Token, column: Token, level: Token) -> None:
        self.table = table
        self.column = column
        self.level = level

    def pprint(self) -> str:
        return f"""
Hierarchy (
    table: {self.table.text},
    column: {self.column.text},
    level: {self.level.text}
)""".strip()

    @classmethod
    @lexer_reset
    def match(cls, parser: "Parser") -> "HierarchyExpression | None":
        table, column, period, level = (
            parser.consume(),
            parser.consume(),
            parser.consume(),
            parser.consume(),
        )
        if table.tok_type not in {
            TokenType.SINGLE_QUOTED_IDENTIFIER,
            TokenType.UNQUOTED_IDENTIFIER,
        }:
            return None
        if column.tok_type != TokenType.BRACKETED_IDENTIFIER:
            return None
        if period.tok_type != TokenType.PERIOD:
            return None
        if level.tok_type != TokenType.BRACKETED_IDENTIFIER:
            return None
        return HierarchyExpression(table=table, column=column, level=level)

    def children(self) -> list[Expression]:  # noqa: PLR6301
        """Returns a list of child expressions."""
        return []

    def position(self) -> tuple[int, int]:
        return self.table.text_slice.start, self.level.text_slice.end

    def full_text(self) -> str:
        return self.table.text_slice.full_text
