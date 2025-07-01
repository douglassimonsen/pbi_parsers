import textwrap
from typing import TYPE_CHECKING

from ..tokens import Token, TokenType
from ._base import Expression
from ._utils import scanner_reset
from .row_index import RowIndexExpression

if TYPE_CHECKING:
    from ..parser import Parser


class RowExpression(Expression):
    table: Token
    indexer: Expression
    row_indexer: RowIndexExpression | None

    def __init__(
        self,
        table: Token,
        indexer: Expression,
        row_indexer: RowIndexExpression | None = None,
    ):
        self.table = table
        self.indexer = indexer
        self.row_indexer = row_indexer

    def pprint(self) -> str:
        indexer = textwrap.indent(self.indexer.pprint(), " " * 4)[4:]
        row_indexer = (
            textwrap.indent(self.row_indexer.pprint(), " " * 4)[4:]
            if self.row_indexer
            else "N/A"
        )
        base = f"""
Table (
    name: {self.table.text},
    indexer: {indexer}
    row_indexer: {row_indexer}
)        """.strip()
        return base

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "FunctionExpression | None":
        from . import any_expression_match

        table = parser.consume()
        if table.type != TokenType.UNQUOTED_IDENTIFIER:
            return None
        if parser.consume().type != TokenType.LEFT_CURLY_BRACE:
            return None
        indexer = any_expression_match(parser)
        if indexer is None:
            return None
        if parser.consume().type != TokenType.RIGHT_CURLY_BRACE:
            return None

        row_indexer = RowIndexExpression.match(parser)
        return RowExpression(table=table, indexer=indexer, row_indexer=row_indexer)
