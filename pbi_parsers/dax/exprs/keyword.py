from typing import TYPE_CHECKING

from pbi_parsers.dax.tokens import KEYWORD_MAPPING, Token, TokenType

from ._base import Expression
from ._utils import scanner_reset
from .function import FunctionExpression

if TYPE_CHECKING:
    from pbi_parsers.dax.parser import Parser


class KeywordExpression(Expression):
    name: Token

    def __init__(self, name: Token) -> None:
        self.name = name

    def pprint(self) -> str:
        return f"""
Keyword ({self.name.text})""".strip()

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "KeywordExpression | FunctionExpression | None":
        name = parser.consume()
        if name.tok_type not in KEYWORD_MAPPING.values():
            return None
        if name.text.lower() in {"true", "false"}:
            p1 = parser.peek()
            p2 = parser.peek(1)
            if (p1.tok_type, p2.tok_type) == (TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN):
                # This is a special case for boolean keywords with parentheses.
                # IDK why microsoft made TRUE() a function too
                left_paren = parser.consume()
                right_paren = parser.consume()
                return FunctionExpression(
                    name_parts=[name],
                    args=[],
                    parens=(left_paren, right_paren),
                )
        return KeywordExpression(name=name)

    def children(self) -> list[Expression]:  # noqa: PLR6301
        """Returns a list of child expressions."""
        return []

    def position(self) -> tuple[int, int]:
        return self.name.text_slice.start, self.name.text_slice.end
