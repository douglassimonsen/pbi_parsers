import textwrap
from typing import TYPE_CHECKING

from parser.dax.tokens import TokenType

from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from parser.dax.parser import Parser


class ArrayExpression(Expression):
    elements: list[Expression]

    def __init__(self, elements: list[Expression]) -> None:
        self.elements: list[Expression] = elements

    def pprint(self) -> str:
        elements = ",\n".join(element.pprint() for element in self.elements)
        elements = textwrap.indent(elements, " " * 14)[14:]
        return f"""
Array (
    elements: {elements}
)        """.strip()

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "ArrayExpression | None":
        from . import any_expression_match  # noqa: PLC0415

        if parser.consume().tok_type != TokenType.LEFT_CURLY_BRACE:
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
        _right_brace = parser.consume()
        return ArrayExpression(elements=elements)
