from typing import TYPE_CHECKING

from ..tokens import Token, TokenType
from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from ..parser import Parser


class BuiltinExpression(Expression):
    name_parts: list[Token]

    def __init__(self, name_parts: list[Token]):
        self.name_parts = name_parts

    def pprint(self) -> str:
        name = ".".join(part.text for part in self.name_parts)
        base = f"Builtin ({name})"
        return base

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "BuiltinExpression | None":
        name_parts = [parser.consume()]
        if name_parts[0].type != TokenType.UNQUOTED_IDENTIFIER:
            return None
        while parser.peek().type == TokenType.PERIOD:
            _period, name = parser.consume(), parser.consume()
            if name.type != TokenType.UNQUOTED_IDENTIFIER:
                return None
            name_parts.append(name)

        return BuiltinExpression(name_parts=name_parts)
