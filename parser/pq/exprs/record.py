import textwrap
from typing import TYPE_CHECKING

from ..tokens import Token, TokenType
from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from ..parser import Parser


class RecordExpression(Expression):
    args: list[tuple[Token, Expression]]

    def __init__(self, args: list[tuple[Token, Expression]]):
        self.args = args

    def pprint(self) -> str:
        args = ",\n".join(f"{arg[0].text}: {arg[1].pprint()}" for arg in self.args)
        args = textwrap.indent(args, " " * 4)[4:]
        base = f"""
Record (
    {args}
)        """.strip()
        return base

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "RecordExpression | None":
        from . import any_expression_match

        args: list[tuple[Token, Expression]] = []
        if parser.consume().type != TokenType.LEFT_BRACKET:
            return None

        while parser.peek().type != TokenType.RIGHT_BRACKET:
            name = parser.consume()
            if name.type != TokenType.UNQUOTED_IDENTIFIER:
                return None

            if parser.consume().type != TokenType.EQUAL_SIGN:
                return None

            value = any_expression_match(parser)
            if value is None:
                return None

            args.append((name, value))

            if parser.peek().type == TokenType.COMMA:
                parser.consume()

        parser.consume()  # consume the right bracket
        return RecordExpression(args=args)
