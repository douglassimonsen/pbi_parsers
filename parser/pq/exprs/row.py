import textwrap
from typing import TYPE_CHECKING

from parser.pq.tokens import TokenType

from ._base import Expression
from ._utils import scanner_reset
from .identifier import IdentifierExpression

if TYPE_CHECKING:
    from parser.pq.parser import Parser


class RowExpression(Expression):
    table: IdentifierExpression
    indexer: Expression

    def __init__(
        self,
        table: IdentifierExpression,
        indexer: Expression,
    ) -> None:
        self.table = table
        self.indexer = indexer

    def pprint(self) -> str:
        indexer = textwrap.indent(self.indexer.pprint(), " " * 4)[4:]
        return f"""
Table (
    name: {self.table.pprint()},
    indexer: {indexer}
)        """.strip()

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "RowExpression | None":
        from . import any_expression_match  # noqa: PLC0415

        table = IdentifierExpression.match(parser)
        if table is None:
            return None
        if parser.consume().tok_type != TokenType.LEFT_CURLY_BRACE:
            return None
        indexer = any_expression_match(parser)
        if indexer is None:
            return None
        if parser.consume().tok_type != TokenType.RIGHT_CURLY_BRACE:
            return None

        return RowExpression(table=table, indexer=indexer)
