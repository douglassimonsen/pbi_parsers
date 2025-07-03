import textwrap
from typing import TYPE_CHECKING

from ..tokens import TokenType
from ._base import Expression
from ._utils import scanner_reset
from .identifier import IdentifierExpression
from .none import NoneExpression

if TYPE_CHECKING:
    from ..parser import Parser


class FunctionExpression(Expression):
    name: IdentifierExpression
    args: list[Expression]

    def __init__(self, name: IdentifierExpression, args: list[Expression]):
        self.name = name
        self.args = args

    def pprint(self) -> str:
        args = ",\n".join(arg.pprint() for arg in self.args)
        args = textwrap.indent(args, " " * 10)[10:]
        base = f"""
Function (
    name: {self.name.pprint()},
    args: {args}
)        """.strip()
        return base

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "FunctionExpression | None":
        from . import any_expression_match

        args: list[Expression] = []

        name = IdentifierExpression.match(parser)
        if name is None:
            return None

        if parser.consume().type != TokenType.LEFT_PAREN:
            return None

        while not cls.match_tokens(parser, [TokenType.RIGHT_PAREN]):
            arg = any_expression_match(parser)
            if arg is not None:
                args.append(arg)
            elif parser.peek().type == TokenType.COMMA:
                args.append(NoneExpression())
            else:
                raise ValueError(
                    f"Unexpected token sequence: {parser.peek()}, {parser.index}"
                )

            if not cls.match_tokens(parser, [TokenType.RIGHT_PAREN]):
                assert parser.consume().type == TokenType.COMMA
        _right_paren = parser.consume()
        ret = FunctionExpression(name=name, args=args)
        return ret
