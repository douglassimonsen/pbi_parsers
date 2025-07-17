import textwrap
from typing import TYPE_CHECKING

from ..tokens import Token, TokenType
from ._base import Expression
from ._utils import scanner_reset

if TYPE_CHECKING:
    from ..parser import Parser


# TODO: maybe convert to StatementExpression in the future?
class VariableExpression(Expression):
    var_name: Token
    statement: Expression

    def __init__(self, var_name: Token, statement: Expression):
        self.var_name = var_name
        self.statement = statement

    def pprint(self, depth: int = 0) -> str:
        base = f"""
Variable (
    name: {self.var_name.text},
    statement: {self.statement}
)
""".strip()
        return textwrap.indent(base, " " * (depth * 4))

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "VariableExpression | None":
        from . import any_expression_match

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
            raise ValueError(
                "VariableExpression.match called without valid inner expression"
            )
        return VariableExpression(var_name=var_name, statement=statement)
