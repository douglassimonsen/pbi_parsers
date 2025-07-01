import textwrap
from typing import TYPE_CHECKING

from ..tokens import TokenType
from ._base import Expression
from ._utils import scanner_reset
from .variable import VariableExpression

if TYPE_CHECKING:
    from ..parser import Parser


# TODO: maybe convert to StatementExpression in the future?
class StatementExpression(Expression):
    statements: list[VariableExpression]
    let_expr: Expression

    def __init__(self, let_expr: Expression, statements: list[VariableExpression]):
        self.let_expr = let_expr
        self.statements = statements

    def pprint(self) -> str:
        let_expr = textwrap.indent(self.let_expr.pprint(), " " * 14)[14:]
        statements = textwrap.indent(
            ",\n".join(statement.pprint() for statement in self.statements), " " * 17
        )[17:]
        base = f"""
Statement (
    statements: {statements}
    let_expr: {let_expr}
)
""".strip()
        return base

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "StatementExpression | None":
        from . import any_expression_match

        if parser.consume().type != TokenType.LET:
            return None

        statements = []
        while parser.peek().type != TokenType.IN:
            statements.append(VariableExpression.match(parser))

            if parser.peek().type == TokenType.COMMA:
                parser.consume()
            elif parser.peek().type != TokenType.IN:
                print(parser.remaining())
                print(statements)
                breakpoint()
                raise ValueError(
                    f"Expected a comma or 'in' token, got {parser.peek().type}"
                )
        if not statements:
            return None

        if parser.consume().type != TokenType.IN:
            raise ValueError("Expected 'in' token after let statements")

        in_expr = any_expression_match(parser)
        if in_expr is None:
            raise ValueError("Expected an expression after 'in' token")
        return StatementExpression(statements=statements, let_expr=in_expr)
