import textwrap
from typing import TYPE_CHECKING

from pbi_parsers.dax.tokens import Token, TokenType

from ._base import Expression
from ._utils import scanner_reset
from .none import NoneExpression

if TYPE_CHECKING:
    from pbi_parsers.dax.parser import Parser


class FunctionExpression(Expression):
    name_parts: list[Token]  # necessary for function names with periods
    args: list[Expression]

    def __init__(self, name_parts: list[Token], args: list[Expression]) -> None:
        self.name_parts = name_parts
        self.args = args

    def pprint(self) -> str:
        args = ",\n".join(arg.pprint() for arg in self.args)
        args = textwrap.indent(args, " " * 10)[10:]
        return f"""
Function (
    name: {"".join(x.text for x in self.name_parts)},
    args: {args}
)        """.strip()

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "FunctionExpression | None":
        from . import any_expression_match  # noqa: PLC0415

        args: list[Expression] = []

        name_parts = [parser.consume()]
        if name_parts[0].tok_type != TokenType.UNQUOTED_IDENTIFIER:
            return None

        while parser.peek().tok_type != TokenType.LEFT_PAREN:
            period, name = parser.consume(), parser.consume()
            if name.tok_type != TokenType.UNQUOTED_IDENTIFIER:
                return None
            if period.tok_type != TokenType.PERIOD:
                return None
            name_parts.extend((period, name))

        if parser.consume().tok_type != TokenType.LEFT_PAREN:
            return None

        while not cls.match_tokens(parser, [TokenType.RIGHT_PAREN]):
            arg = any_expression_match(parser)
            if arg is not None:
                args.append(arg)
            elif parser.peek().tok_type == TokenType.COMMA:
                args.append(NoneExpression())
            else:
                msg = f"Unexpected token sequence: {parser.peek()}, {parser.index}"
                raise ValueError(msg)

            if not cls.match_tokens(parser, [TokenType.RIGHT_PAREN]):
                assert parser.consume().tok_type == TokenType.COMMA
        _right_paren = parser.consume()
        return FunctionExpression(name_parts=name_parts, args=args)
