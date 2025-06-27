import textwrap

from typing import TYPE_CHECKING
from ..tokens import Token, TokenType
from ._base import Expression
from .column import ColumnExpression
from .literal_number import LiteralNumberExpression
from .literal_string import LiteralStringExpression
from .measure import MeasureExpression
if TYPE_CHECKING:
    from ..parser import Parser


class FunctionExpression(Expression):
    name: Token
    args: list[Expression]

    def __init__(self, name: Token, args: list[Expression]):
        self.name = name
        self.args = args

    def pprint(self, depth: int = 0) -> str:
        args = ",\n".join(arg.pprint() for arg in self.args)
        args = textwrap.indent(args, " " * 10)[10:]
        base = f"""
Function (
    name: {self.name.text},
    args: {args}
)        """.strip()
        return textwrap.indent(base, " " * (depth * 4))

    @classmethod
    def match(cls, parser: "Parser") -> "FunctionExpression | None":
        if not cls.match_tokens(
            parser, [TokenType.UNQUOTED_IDENTIFIER, TokenType.LEFT_PAREN]
        ):
            return None
        args: list[Expression] = []
        name, _paren = (
            parser.pop(),
            parser.pop(),
        )  # Skip the function name and left parenthesis
        while not cls.match_tokens(parser, [TokenType.RIGHT_PAREN]):
            # We gotta handle operators next :(
            for expr in (
                ColumnExpression,
                MeasureExpression,
                FunctionExpression,
                LiteralStringExpression,
                LiteralNumberExpression,
            ):
                if arg := expr.match(parser):
                    args.append(arg)
                    break
            else:
                breakpoint()
                raise ValueError(f"Unexpected token sequence: {parser.peek()}")
            if not cls.match_tokens(parser, [TokenType.RIGHT_PAREN]):
                assert cls.match_tokens(
                    parser, [TokenType.COMMA]
                ), f"Expected a comma, found: {parser.peek()}"
                parser.pop()
        _right_paren = parser.pop()
        ret = FunctionExpression(name=name, args=args)
        return ret
