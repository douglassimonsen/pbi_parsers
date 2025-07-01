import textwrap
from typing import TYPE_CHECKING

from ..tokens import Token, TokenType
from ._base import Expression
from ._utils import scanner_reset
from .none import NoneExpression

if TYPE_CHECKING:
    from ..parser import Parser


class FunctionExpression(Expression):
    name_parts: list[Token]  # necessary for function names with periods
    args: list[Expression]

    def __init__(self, name_parts: list[Token], args: list[Expression]):
        self.name_parts = name_parts
        self.args = args

    def pprint(self) -> str:
        args = ",\n".join(arg.pprint() for arg in self.args)
        args = textwrap.indent(args, " " * 10)[10:]
        base = f"""
Function (
    name: {"".join(x.text for x in self.name_parts)},
    args: {args}
)        """.strip()
        return base

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "FunctionExpression | None":
        from . import any_expression_match

        args: list[Expression] = []

        name_parts = [parser.consume()]
        if name_parts[0].type != TokenType.UNQUOTED_IDENTIFIER:
            return None

        while parser.peek().type != TokenType.LEFT_PAREN:
            period, name = parser.consume(), parser.consume()
            if name.type != TokenType.UNQUOTED_IDENTIFIER:
                return None
            if period.type != TokenType.PERIOD:
                return None
            name_parts.extend((period, name))

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
        ret = FunctionExpression(name_parts=name_parts, args=args)
        return ret
