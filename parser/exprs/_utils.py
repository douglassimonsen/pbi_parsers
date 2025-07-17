from typing import TYPE_CHECKING, Callable

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


from typing import ParamSpec, TypeVar

P = ParamSpec("P")  # Represents the parameters of the decorated function
R = TypeVar("R")  # Represents the return type of the decorated function


def scanner_reset(func: Callable[P, R]) -> Callable[P, R]:
    def scanner_reset_inner(*args: P.args, **kwargs: P.kwargs) -> R:
        parser: Parser = args[1]
        idx = parser.index
        ret = func(*args, **kwargs)
        if ret is None:
            parser.index = idx
        return ret

    return scanner_reset_inner
