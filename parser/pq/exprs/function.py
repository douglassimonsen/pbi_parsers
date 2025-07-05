import textwrap
from typing import TYPE_CHECKING

from parser.pq.tokens import TokenType

from ._base import Expression
from ._utils import scanner_reset
from .identifier import IdentifierExpression
from .none import NoneExpression

if TYPE_CHECKING:
    from parser.pq.parser import Parser


class FunctionExpression(Expression):
    name: IdentifierExpression
    args: list[Expression]

    def __init__(self, name: IdentifierExpression, args: list[Expression]) -> None:
        self.name = name
        self.args = args

    def pprint(self) -> str:
        args = ",\n".join(arg.pprint() for arg in self.args)
        args = textwrap.indent(args, " " * 10)[10:]
        return f"""
Function (
    name: {self.name.pprint()},
    args: {args}
)        """.strip()

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "FunctionExpression | None":
        from . import any_expression_match  # noqa: PLC0415

        args: list[Expression] = []

        name = IdentifierExpression.match(parser)
        if name is None:
            return None

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
        return FunctionExpression(name=name, args=args)
