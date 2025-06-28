from typing import TYPE_CHECKING, Callable, ParamSpec, TypeVar

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


P = ParamSpec("P")  # Represents the parameters of the decorated function
R = TypeVar("R")  # Represents the return type of the decorated function


cache: dict[tuple[int, int], tuple[Expression | None, int]] = {}


def scanner_reset(func: Callable[P, R]) -> Callable[P, R]:
    def scanner_reset_inner(*args: P.args, **kwargs: P.kwargs) -> R:
        parser: "Parser" = args[1]  # type: ignore
        idx = parser.index

        # Speed up of a bazillion
        cached_val, cached_index = cache.get((idx, id(func)), (None, -1))
        if cached_val is not None:
            parser.index = cached_index
            return cached_val  # type: ignore

        ret = func(*args, **kwargs)

        cache[(idx, id(func))] = (ret, parser.index)  # type: ignore
        if ret is None:
            parser.index = idx
        return ret

    return scanner_reset_inner
