import textwrap
from typing import TYPE_CHECKING

from ..tokens import Token, TokenType
from ._base import Expression
from ._utils import scanner_reset

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
    @scanner_reset
    def match(cls, parser: "Parser") -> "FunctionExpression | None":
        from . import any_expression_match

        if not cls.match_tokens(
            parser, [TokenType.UNQUOTED_IDENTIFIER, TokenType.LEFT_PAREN]
        ):
            return None

        args: list[Expression] = []
        name, _paren = (
            parser.consume(),
            parser.consume(),
        )  # Skip the function name and left parenthesis
        while not cls.match_tokens(parser, [TokenType.RIGHT_PAREN]):
            # We gotta handle operators next :(
            arg = any_expression_match(parser)
            print(arg)
            if arg is not None:
                args.append(arg)
            else:
                raise ValueError(
                    f"Unexpected token sequence: {parser.peek()}, {parser.index}"
                )

            if not cls.match_tokens(parser, [TokenType.RIGHT_PAREN]):
                assert parser.consume().type == TokenType.COMMA
        _right_paren = parser.consume()
        ret = FunctionExpression(name=name, args=args)
        return ret
