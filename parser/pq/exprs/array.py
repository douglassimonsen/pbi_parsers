import textwrap
from typing import TYPE_CHECKING

from ..tokens import TokenType
from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from ..parser import Parser


class ArrayExpression(Expression):
    elements: list[Expression]

    def __init__(self, elements: list[Expression]):
        self.elements: list[Expression] = elements

    def pprint(self) -> str:
        elements = ",\n".join(element.pprint() for element in self.elements)
        elements = textwrap.indent(elements, " " * 14)[14:]
        base = f"""
Array (
    elements: {elements}
)        """.strip()
        return base

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "ArrayExpression | None":
        from . import any_expression_match

        if parser.consume().type != TokenType.LEFT_CURLY_BRACE:
            return None

        elements: list[Expression] = []

        while not cls.match_tokens(parser, [TokenType.RIGHT_CURLY_BRACE]):
            # We gotta handle operators next :(
            element = any_expression_match(parser)
            if element is not None:
                elements.append(element)
            else:
                raise ValueError(
                    f"Unexpected token sequence: {parser.peek()}, {parser.index}"
                )

            if not cls.match_tokens(parser, [TokenType.RIGHT_CURLY_BRACE]):
                assert parser.consume().type == TokenType.COMMA
        _right_brace = parser.consume()
        ret = ArrayExpression(elements=elements)
        return ret
