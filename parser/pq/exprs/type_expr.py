import textwrap
from typing import TYPE_CHECKING

from ..tokens import Token, TokenType
from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from ..parser import Parser


class TypingExpression(Expression):
    type_name: list[Token]
    column_mapping: Expression | None = None

    def __init__(
        self, type_name: list[Token], column_mapping: Expression | None = None
    ):
        self.type_name = type_name
        self.column_mapping = column_mapping

    def pprint(self) -> str:
        type_name = ".".join(t.text for t in self.type_name)
        if self.column_mapping is None:
            base = f"Type ({type_name})"
        else:
            column_mapping = textwrap.indent(self.column_mapping.pprint(), " " * 10)[
                10:
            ]
            base = f"""
Type (
    type: {type_name},
    column: {column_mapping}
)
"""
        return base

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "TypingExpression | None":
        from . import any_expression_match

        type_keyword = parser.consume()
        if type_keyword.type == TokenType.TYPE_LITERAL:
            return TypingExpression(type_name=[type_keyword])
        if type_keyword.type != TokenType.TYPE:
            return None

        name_parts = [parser.consume()]
        # single part name (i.e. no period)
        while parser.peek().type == TokenType.PERIOD:
            period, name = parser.consume(), parser.consume()
            if name.type not in (TokenType.UNQUOTED_IDENTIFIER, TokenType.TYPE):
                return None
            if period.type != TokenType.PERIOD:
                return None
            name_parts.append(name)
        if len(name_parts) == 1 and name_parts[0].text == "table":
            column_mapping = any_expression_match(parser)
        else:
            column_mapping = None
        return TypingExpression(type_name=name_parts, column_mapping=column_mapping)
