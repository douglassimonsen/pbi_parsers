import textwrap
from typing import TYPE_CHECKING

from pbi_parsers.pq.tokens import TokenType

from ._base import Expression
from ._utils import scanner_reset
from .identifier import IdentifierExpression

if TYPE_CHECKING:
    from pbi_parsers.pq.parser import Parser


class RecordExpression(Expression):
    args: list[tuple[IdentifierExpression, Expression]]

    def __init__(self, args: list[tuple[IdentifierExpression, Expression]]) -> None:
        self.args = args

    def pprint(self) -> str:
        args = ",\n".join(f"{arg[0].pprint()}: {arg[1].pprint()}" for arg in self.args)
        args = textwrap.indent(args, " " * 4)[4:]
        return f"""
Record (
    {args}
)        """.strip()

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "RecordExpression | None":
        from . import any_expression_match  # noqa: PLC0415

        args: list[tuple[IdentifierExpression, Expression]] = []
        if parser.consume().tok_type != TokenType.LEFT_BRACKET:
            return None

        while parser.peek().tok_type != TokenType.RIGHT_BRACKET:
            name = IdentifierExpression.match(parser)
            if name is None:
                return None
            if parser.consume().tok_type != TokenType.EQUAL_SIGN:
                return None

            value = any_expression_match(parser)
            if value is None:
                return None

            args.append((name, value))

            if parser.peek().tok_type == TokenType.COMMA:
                parser.consume()

        parser.consume()  # consume the right bracket
        return RecordExpression(args=args)
