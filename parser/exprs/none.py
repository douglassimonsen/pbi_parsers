from typing import TYPE_CHECKING

from ._base import Expression

if TYPE_CHECKING:
    from ..parser import Parser


class NoneExpression(Expression):
    """
    This is used to represent the absence of a value, so far only occurring when a argument is skipped in a function.
    """

    def pprint(self) -> str:
        return "None"

    @classmethod
    def match(cls, parser: "Parser") -> "NoneExpression | None":
        raise NotImplementedError(
            "NoneExpression.match should not be called, this is a placeholder for the absence of an expression."
        )
