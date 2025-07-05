import textwrap
from typing import TYPE_CHECKING

from parser.dax.tokens import TokenType

from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from parser.dax.parser import Parser


class ExponentExpression(Expression):
    """Represents an addition or subtraction expression."""

    base: Expression
    power: Expression

    def __init__(self, base: Expression, power: Expression) -> None:
        self.base = base
        self.power = power

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "ExponentExpression | None":
        from . import EXPRESSION_HIERARCHY, any_expression_match  # noqa: PLC0415

        skip_index = EXPRESSION_HIERARCHY.index(ExponentExpression)

        base = any_expression_match(parser=parser, skip_first=skip_index + 1)
        operator = parser.consume()

        if not base:
            return None
        if operator.tok_type != TokenType.EXPONENTIATION_SIGN:
            return None

        power = any_expression_match(parser=parser, skip_first=skip_index)
        if power is None:
            msg = f"Expected a power term after operator {operator.text}, found: {parser.peek()}"
            raise ValueError(msg)
        return ExponentExpression(base=base, power=power)

    def pprint(self) -> str:
        base_str = textwrap.indent(self.base.pprint(), " " * 10).lstrip()
        power_str = textwrap.indent(self.power.pprint(), " " * 10).lstrip()
        return f"""
Exponent (
    base: {base_str},
    power: {power_str}
)""".strip()
