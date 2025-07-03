from typing import TYPE_CHECKING

from ..tokens import TokenType
from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from ..parser import Parser


class EllipsisExpression(Expression):
    def __init__(self):
        pass

    def pprint(self) -> str:
        base = "Ellipsis ()"
        return base

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "EllipsisExpression | None":
        if not parser.consume().type == TokenType.ELLIPSIS:
            return None
        return EllipsisExpression()
