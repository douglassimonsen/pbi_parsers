from typing import TYPE_CHECKING

from pbi_parsers.dax.tokens import Token, TokenType

from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from pbi_parsers.dax.parser import Parser


class MeasureExpression(Expression):
    name: Token

    def __init__(self, name: Token) -> None:
        self.name = name

    def pprint(self) -> str:
        return f"Measure ({self.name.text})"

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "MeasureExpression | None":
        if cls.match_tokens(parser, [TokenType.BRACKETED_IDENTIFIER]):
            name = parser.consume()
            return MeasureExpression(name=name)
        return None

    def children(self) -> list[Expression]:  # noqa: PLR6301
        """Returns a list of child expressions."""
        return []

    def position(self) -> tuple[int, int]:
        return self.name.text_slice.start, self.name.text_slice.end
