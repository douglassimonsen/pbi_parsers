from typing import TYPE_CHECKING

from pbi_parsers.pq.tokens import Token, TokenType

from ._base import Expression
from ._utils import lexer_reset

if TYPE_CHECKING:
    from pbi_parsers.pq.parser import Parser


class KeywordExpression(Expression):
    name: Token

    def __init__(self, name: Token) -> None:
        self.name = name

    def pprint(self) -> str:
        return f"""
Keyword ({self.name.text})""".strip()

    @classmethod
    @lexer_reset
    def match(cls, parser: "Parser") -> "KeywordExpression | None":
        name = parser.consume()
        if name.tok_type != TokenType.KEYWORD:
            return None
        if name.text.lower() in {"true", "false"}:
            p1 = parser.peek()
            p2 = parser.peek(1)
            if p1.tok_type == TokenType.LEFT_PAREN and p2.tok_type == TokenType.RIGHT_PAREN:
                # This is a special case for boolean keywords with parentheses.
                # IDK why microsoft made TRUE() a function too
                parser.consume()
                parser.consume()
        return KeywordExpression(name=name)

    def children(self) -> list[Expression]:  # noqa: PLR6301
        """Returns a list of child expressions."""
        return []
