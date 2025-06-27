from typing import TYPE_CHECKING

from ._base import Expression

if TYPE_CHECKING:
    from ..parser import Parser


def or_match(
    exprs: tuple[type[Expression], ...], parser: "Parser"
) -> Expression | None:
    """
    Match non-operator expressions like Column, Measure, Function, LiteralString, and LiteralNumber.
    """
    for expr in exprs:
        if ret := expr.match(parser):
            return ret
    return None
