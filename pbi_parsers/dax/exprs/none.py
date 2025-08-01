from typing import TYPE_CHECKING

from ._base import Expression

if TYPE_CHECKING:
    from pbi_parsers.dax.parser import Parser


class NoneExpression(Expression):
    """Used to represent the absence of a value, so far only occurring when a argument is skipped in a function."""

    def children(self) -> list[Expression]:  # noqa: PLR6301
        """Returns a list of child expressions."""
        return []

    def full_text(self) -> str:  # noqa: PLR6301
        """Returns the full text of the expression."""
        return ""

    @classmethod
    def match(cls, parser: "Parser") -> "NoneExpression | None":
        msg = "NoneExpression.match should not be called, this is a placeholder for the absence of an expression."
        raise NotImplementedError(msg)

    def position(self) -> tuple[int, int]:  # noqa: PLR6301
        """Returns the position of the expression."""
        return -1, -1

    def pprint(self) -> str:  # noqa: PLR6301  # kept this way to match the interface
        return "None"
