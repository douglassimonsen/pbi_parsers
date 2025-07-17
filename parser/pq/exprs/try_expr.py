import textwrap
from typing import TYPE_CHECKING

from ..tokens import TokenType
from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from ..parser import Parser


class TryExpression(Expression):
    try_expr: Expression
    otherwise_expr: Expression

    def __init__(self, try_expr: Expression, otherwise_expr: Expression):
        self.try_expr = try_expr
        self.otherwise_expr = otherwise_expr

    def pprint(self) -> str:
        try_expr = textwrap.indent(self.try_expr.pprint(), " " * 10)[10:]
        otherwise_expr = textwrap.indent(self.otherwise_expr.pprint(), " " * 10)[10:]
        base = f"""
Try (
    try: {try_expr},
    otherwise: {otherwise_expr}
)""".strip()
        return base

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "TryExpression | None":
        from . import any_expression_match

        _try = parser.consume()
        if _try.type != TokenType.TRY:
            return None
        try_expr: Expression | None = any_expression_match(
            parser
        )  # this expression can recurse
        if not try_expr:
            return None

        _otherwise = parser.consume()
        if _otherwise.type != TokenType.OTHERWISE:
            return None
        otherwise_expr = any_expression_match(parser)
        if not otherwise_expr:
            return None

        return TryExpression(try_expr=try_expr, otherwise_expr=otherwise_expr)
