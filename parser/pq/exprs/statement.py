import textwrap
from typing import TYPE_CHECKING

from parser.pq.tokens import TokenType

from ._base import Expression
from ._utils import scanner_reset
from .variable import VariableExpression

if TYPE_CHECKING:
    from parser.pq.parser import Parser


class StatementExpression(Expression):
    statements: list[VariableExpression]
    let_expr: Expression

    def __init__(self, let_expr: Expression, statements: list[VariableExpression]) -> None:
        self.let_expr = let_expr
        self.statements = statements

    def pprint(self) -> str:
        let_expr = textwrap.indent(self.let_expr.pprint(), " " * 14)[14:]
        statements = textwrap.indent(
            ",\n".join(statement.pprint() for statement in self.statements),
            " " * 17,
        )[17:]
        return f"""
Statement (
    statements: {statements}
    let_expr: {let_expr}
)
""".strip()

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "StatementExpression | None":
        from . import any_expression_match  # noqa: PLC0415

        if parser.consume().tok_type != TokenType.LET:
            return None

        statements = []
        while parser.peek().tok_type != TokenType.IN:
            statements.append(VariableExpression.match(parser))

            if parser.peek().tok_type == TokenType.COMMA:
                parser.consume()
            elif parser.peek().tok_type != TokenType.IN:
                print(parser.remaining())
                print(statements)
                exit()
                msg = f"Expected a comma or 'in' token, got {parser.peek().tok_type}"
                raise ValueError(msg)
        if not statements:
            return None

        if parser.consume().tok_type != TokenType.IN:
            msg = "Expected 'in' token after let statements"
            raise ValueError(msg)

        in_expr = any_expression_match(parser)
        if in_expr is None:
            msg = "Expected an expression after 'in' token"
            raise ValueError(msg)
        return StatementExpression(statements=statements, let_expr=in_expr)
