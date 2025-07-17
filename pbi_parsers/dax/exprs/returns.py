import textwrap
from typing import TYPE_CHECKING

from pbi_parsers.dax.tokens import TokenType

from ._base import Expression
from ._utils import scanner_reset
from .variable import VariableExpression

if TYPE_CHECKING:
    from pbi_parsers.dax.parser import Parser


class ReturnExpression(Expression):
    ret: Expression
    variable_statements: list[Expression]

    def __init__(self, ret: Expression, variable_statements: list[Expression]) -> None:
        self.ret = ret
        self.variable_statements = variable_statements

    def pprint(self) -> str:
        return_val = textwrap.indent(self.ret.pprint(), " " * 12).lstrip()
        statements = textwrap.indent(
            ",\n".join(stmt.pprint() for stmt in self.variable_statements),
            " " * 16,
        ).lstrip()
        return f"""
Return (
    Return: {return_val},
    Statements: {statements}
)""".strip()

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "ReturnExpression | None":
        from . import any_expression_match  # noqa: PLC0415

        if not cls.match_tokens(parser, [TokenType.VARIABLE]):
            return None

        statements: list[Expression] = []
        while not cls.match_tokens(parser, [TokenType.RETURN]):
            statement = VariableExpression.match(parser)
            if statement is None:
                msg = "ReturnExpression.match called without valid inner expression"
                raise ValueError(msg)
            statements.append(statement)

        assert parser.consume().tok_type == TokenType.RETURN  # Consume the return token
        ret = any_expression_match(parser)
        if ret is None:
            msg = "ReturnExpression.match called without valid return expression"
            raise ValueError(msg)
        return ReturnExpression(ret=ret, variable_statements=statements)

    def children(self) -> list[Expression]:
        """Returns a list of child expressions."""
        return [self.ret, *self.variable_statements]

    def position(self) -> tuple[int, int]:
        return self.variable_statements[0].position()[0], self.ret.position()[1]
