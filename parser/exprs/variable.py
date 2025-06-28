import textwrap
from typing import TYPE_CHECKING

from ..tokens import Token
from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from ..parser import Parser


# TODO: maybe convert to StatementExpression in the future?
class VariableExpression(Expression):
    var_name: Token
    statement: Expression

    def __init__(self, value: Token):
        self.value = value

    def pprint(self, depth: int = 0) -> str:
        base = f" ({self.value.text})"
        return textwrap.indent(base, " " * (depth * 4))

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "VariableExpression | None":
        breakpoint()
