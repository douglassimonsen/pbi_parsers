import textwrap
from typing import TYPE_CHECKING

from pbi_parsers.dax.tokens import Token, TokenType

from ._base import Expression
from ._utils import lexer_reset

if TYPE_CHECKING:
    from pbi_parsers.dax.parser import Parser


class ArrayExpression(Expression):
    elements: list[Expression]
    braces: tuple[Token, Token]

    def __init__(self, elements: list[Expression], braces: tuple[Token, Token]) -> None:
        self.elements: list[Expression] = elements
        self.braces = braces

    def pprint(self) -> str:
        elements = ",\n".join(element.pprint() for element in self.elements)
        elements = textwrap.indent(elements, " " * 14)[14:]
        return f"""
Array (
    elements: {elements}
)        """.strip()

    @classmethod
    @lexer_reset
    def match(cls, parser: "Parser") -> "ArrayExpression | None":
        from . import any_expression_match  # noqa: PLC0415

        left_brace = parser.consume()
        if left_brace.tok_type != TokenType.LEFT_CURLY_BRACE:
            return None

        elements: list[Expression] = []

        while not cls.match_tokens(parser, [TokenType.RIGHT_CURLY_BRACE]):
            # We gotta handle operators next :(
            element = any_expression_match(parser)
            if element is not None:
                elements.append(element)
            else:
                msg = f"Unexpected token sequence: {parser.peek()}, {parser.index}"
                raise ValueError(msg)

            if not cls.match_tokens(parser, [TokenType.RIGHT_CURLY_BRACE]):
                assert parser.consume().tok_type == TokenType.COMMA

        right_brace = parser.consume()
        if right_brace.tok_type != TokenType.RIGHT_CURLY_BRACE:
            msg = f"Expected a right curly brace, found: {right_brace}"
            raise ValueError(msg)

        return ArrayExpression(elements=elements, braces=(left_brace, right_brace))

    def children(self) -> list[Expression]:
        """Returns a list of child expressions."""
        return self.elements

    def position(self) -> tuple[int, int]:
        return self.braces[0].text_slice.start, self.braces[1].text_slice.end

    def full_text(self) -> str:
        return self.braces[0].text_slice.full_text
