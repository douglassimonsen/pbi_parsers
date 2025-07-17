import textwrap
from typing import TYPE_CHECKING

from pbi_parsers.dax.tokens import Token, TokenType

from ._base import Expression
from ._utils import lexer_reset

if TYPE_CHECKING:
    from pbi_parsers.dax.parser import Parser


class VariableExpression(Expression):
    """Represents a variable assignment in DAX.

    Examples:
        VAR x = 1
        VAR y = x + 2

        VAR z = func()

    """

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
    @lexer_reset
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

    def children(self) -> list[Expression]:
        """Returns a list of child expressions."""
        return [self.statement]

    def position(self) -> tuple[int, int]:
        return self.var_name.text_slice.start, self.statement.position()[1]

    def full_text(self) -> str:
        return self.var_name.text_slice.full_text
