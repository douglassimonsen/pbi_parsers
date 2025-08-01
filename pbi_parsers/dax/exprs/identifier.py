from typing import TYPE_CHECKING

from pbi_parsers.dax.tokens import Token, TokenType

from ._base import Expression
from ._utils import lexer_reset

if TYPE_CHECKING:
    from pbi_parsers.dax.parser import Parser


class IdentifierExpression(Expression):
    """Represents a simple identifier of a variable.

    Examples:
        VariableName
        AnotherVariableName

    """

    name: Token

    def __init__(self, name: Token) -> None:
        self.name = name

    def children(self) -> list[Expression]:  # noqa: PLR6301
        """Returns a list of child expressions."""
        return []

    def full_text(self) -> str:
        return self.name.text_slice.full_text

    @classmethod
    @lexer_reset
    def match(cls, parser: "Parser") -> "IdentifierExpression | None":
        name = parser.consume()
        if name.tok_type != TokenType.UNQUOTED_IDENTIFIER:
            return None
        return IdentifierExpression(name=name)

    def position(self) -> tuple[int, int]:
        return self.name.text_slice.start, self.name.text_slice.end

    def pprint(self) -> str:
        return f"""
Identifier ({self.name.text})""".strip()
