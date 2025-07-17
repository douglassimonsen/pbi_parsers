import textwrap
from typing import TYPE_CHECKING

from ..tokens import TokenType
from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from ..parser import Parser


class RowIndexExpression(Expression):
    indexer: Expression

    def __init__(self, indexer: Expression):
        self.indexer = indexer

    def pprint(self) -> str:
        indexer = textwrap.indent(self.indexer.pprint(), " " * 4)[4:]
        base = f"""
Indexer (
    expr: {indexer}
)        """.strip()
        return base

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "RowIndexExpression | None":
        from . import any_expression_match

        if parser.consume().type != TokenType.LEFT_BRACKET:
            return None

        indexer = any_expression_match(parser)
        if indexer is None:
            return None

        if parser.consume().type != TokenType.RIGHT_BRACKET:
            return None

        return RowIndexExpression(indexer=indexer)
