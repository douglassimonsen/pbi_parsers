import textwrap
from typing import TYPE_CHECKING

from parser.pq.tokens import TokenType

from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from parser.pq.parser import Parser


class RowIndexExpression(Expression):
    table: Expression
    indexer: Expression

    def __init__(self, table: Expression, indexer: Expression) -> None:
        self.table = table
        self.indexer = indexer

    def pprint(self) -> str:
        table = textwrap.indent(self.table.pprint(), " " * 4)[4:]
        indexer = textwrap.indent(self.indexer.pprint(), " " * 4)[4:]
        return f"""
Indexer (
    table: {table},
    indexer: {indexer}
)        """.strip()

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "RowIndexExpression | None":
        from . import EXPRESSION_HIERARCHY, any_expression_match  # noqa: PLC0415

        skip_index = EXPRESSION_HIERARCHY.index(
            RowIndexExpression,
        )  # intentionally inclusive of self to allow +-++- chains

        table = any_expression_match(parser, skip_first=skip_index + 1)
        if table is None:
            return None

        if parser.consume().tok_type != TokenType.LEFT_BRACKET:
            return None

        indexer = any_expression_match(parser)
        if indexer is None:
            return None

        if parser.consume().tok_type != TokenType.RIGHT_BRACKET:
            return None

        return RowIndexExpression(table=table, indexer=indexer)
