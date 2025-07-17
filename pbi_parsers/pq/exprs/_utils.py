from collections.abc import Callable
from typing import ParamSpec, TypeVar

from pbi_parsers.pq.parser import Parser

P = ParamSpec("P")  # Represents the parameters of the decorated function
R = TypeVar("R")  # Represents the return type of the decorated function


def lexer_reset(func: Callable[P, R]) -> Callable[P, R]:
    def lexer_reset_inner(*args: P.args, **kwargs: P.kwargs) -> R:
        parser = args[1]
        if not isinstance(parser, Parser):
            msg = f"Expected the second argument to be a Parser instance, got {type(parser)}"
            raise TypeError(msg)
        idx = parser.index

        # Speed up of a bazillion
        cached_val, cached_index = parser.cache.get((idx, id(func)), (None, -1))
        if cached_val is not None:
            parser.index = cached_index
            return cached_val

        ret = func(*args, **kwargs)

        parser.cache[idx, id(func)] = (ret, parser.index)
        if ret is None:
            parser.index = idx
        return ret

    return lexer_reset_inner
