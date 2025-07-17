import textwrap
from typing import TYPE_CHECKING

from ..tokens import TokenType
from ._base import Expression
from ._utils import scanner_reset
from .variable import VariableExpression

if TYPE_CHECKING:
    from ..parser import Parser


class ReturnExpression(Expression):
    ret: Expression
    variable_statements: list[Expression]

    def __init__(self, ret: Expression, variable_statements: list[Expression]):
        self.ret = ret
        self.variable_statements = variable_statements

    def pprint(self):
        return_val = textwrap.indent(self.ret.pprint(), " " * 13).lstrip()
        statements = textwrap.indent(
            ",\n".join(stmt.pprint() for stmt in self.variable_statements), " " * 17
        ).lstrip()
        base = f"""
Return (
    Return: {return_val},
    Statements: {statements}
)""".strip()
        return base

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "ReturnExpression | None":
        from . import any_expression_match

        if not cls.match_tokens(parser, [TokenType.VARIABLE]):
            return None

        statements: list[Expression] = []
        while not cls.match_tokens(parser, [TokenType.RETURN]):
            statement = VariableExpression.match(parser)
            if statement is None:
                raise ValueError(
                    "ReturnExpression.match called without valid inner expression"
                )
            statements.append(statement)

        assert parser.consume().type == TokenType.RETURN  # Consume the return token
        ret = any_expression_match(parser)
        if ret is None:
            raise ValueError(
                "ReturnExpression.match called without valid return expression"
            )
        return ReturnExpression(ret=ret, variable_statements=statements)
