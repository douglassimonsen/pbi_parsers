import textwrap
from typing import TYPE_CHECKING

from pbi_parsers.dax.tokens import Token, TokenType

from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from pbi_parsers.dax.parser import Parser


class VariableExpression(Expression):
    var_name: Token
    statement: Expression

    def __init__(self, var_name: Token, statement: Expression) -> None:
        self.var_name = var_name
        self.statement = statement

    def pprint(self) -> str:
        statement = textwrap.indent(self.statement.pprint(), " " * 15).lstrip()
        return f"""
Variable (
    name: {self.var_name.text},
    statement: {statement}
)
""".strip()

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "VariableExpression | None":
        from . import any_expression_match  # noqa: PLC0415

        if not cls.match_tokens(
            parser,
            [TokenType.VARIABLE, TokenType.UNQUOTED_IDENTIFIER, TokenType.EQUAL_SIGN],
        ):
            return None

        parser.consume()
        var_name = parser.consume()
        parser.consume()
        statement = any_expression_match(parser)
        if statement is None:
            msg = "VariableExpression.match called without valid inner expression"
            raise ValueError(msg)
        return VariableExpression(var_name=var_name, statement=statement)
