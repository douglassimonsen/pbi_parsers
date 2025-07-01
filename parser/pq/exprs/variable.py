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

    def pprint(self) -> str:
        statement = textwrap.indent(self.statement.pprint(), " " * 17).lstrip()
        base = f"""
Variable (
    name: {self.var_name.text},
    statement: {statement}
)
""".strip()
        return base

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "VariableExpression | None":
        from . import any_expression_match

        var_name = parser.consume()
        _equal_sign = parser.consume()
        if (
            var_name.type
            not in (TokenType.QUOTED_IDENTIFER, TokenType.UNQUOTED_IDENTIFIER)
            or _equal_sign.type != TokenType.EQUAL_SIGN
        ):
            return None

        statement = any_expression_match(parser)
        if statement is None:
            raise ValueError(
                "VariableExpression.match called without valid inner expression"
            )
        return VariableExpression(var_name=var_name, statement=statement)
