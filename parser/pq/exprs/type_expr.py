from typing import TYPE_CHECKING

from ..tokens import Token, TokenType
from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from ..parser import Parser


class TypingExpression(Expression):
    type_name: list[Token]

    def __init__(self, type_name: list[Token]):
        self.type_name = type_name

    def pprint(self) -> str:
        type_name = ".".join(t.text for t in self.type_name)
        base = f"Type ({type_name})"
        return base

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "TypingExpression | None":
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
        return TypingExpression(type_name=name_parts)
