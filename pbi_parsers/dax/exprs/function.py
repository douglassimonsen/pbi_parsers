import textwrap
from typing import TYPE_CHECKING

from pbi_parsers.dax.tokens import Token, TokenType

from ._base import Expression
from ._utils import lexer_reset
from .none import NoneExpression

if TYPE_CHECKING:
    from pbi_parsers.dax.parser import Parser


class FunctionExpression(Expression):
    name_parts: list[Token]  # necessary for function names with periods
    args: list[Expression]
    parens: tuple[Token, Token]  # left and right parentheses

    def __init__(self, name_parts: list[Token], args: list[Expression], parens: tuple[Token, Token]) -> None:
        self.name_parts = name_parts
        self.args = args
        self.parens = parens

    def pprint(self) -> str:
        args = ",\n".join(arg.pprint() for arg in self.args)
        args = textwrap.indent(args, " " * 10)[10:]
        return f"""
Function (
    name: {"".join(x.text for x in self.name_parts)},
    args: {args}
)        """.strip()

    @classmethod
    @lexer_reset
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

        left_paren = parser.consume()
        if left_paren.tok_type != TokenType.LEFT_PAREN:
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

        right_paren = parser.consume()
        if right_paren.tok_type != TokenType.RIGHT_PAREN:
            msg = f"Expected a right parenthesis, found: {right_paren}"
            raise ValueError(msg)

        return FunctionExpression(name_parts=name_parts, args=args, parens=(left_paren, right_paren))

    def function_name(self) -> str:
        return "".join(x.text for x in self.name_parts)

    def children(self) -> list[Expression]:
        """Returns a list of child expressions."""
        return self.args

    def position(self) -> tuple[int, int]:
        return self.parens[0].text_slice.start, self.parens[1].text_slice.end

    def full_text(self) -> str:
        return self.parens[0].text_slice.full_text
