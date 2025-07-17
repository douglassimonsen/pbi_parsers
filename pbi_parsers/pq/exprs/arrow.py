import textwrap
from typing import TYPE_CHECKING

from pbi_parsers.pq.tokens import TokenType

from ._base import Expression
from ._utils import scanner_reset
from .parens import ParenthesesExpression

if TYPE_CHECKING:
    from pbi_parsers.pq.parser import Parser


class ArrowExpression(Expression):
    inputs: ParenthesesExpression
    function_body: Expression

    def __init__(self, inputs: ParenthesesExpression, function_body: Expression) -> None:
        self.inputs = inputs
        self.function_body = function_body

    def pprint(self) -> str:
        inputs = textwrap.indent(self.inputs.pprint(), " " * 10)[10:]
        function_body = textwrap.indent(self.function_body.pprint(), " " * 10)[10:]
        return f"""
Arrow (
    inputs: {inputs},
    function_body: {function_body}
)""".strip()

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "ArrowExpression | None":
        from . import any_expression_match  # noqa: PLC0415

        inputs = ParenthesesExpression.match(parser)
        if inputs is None:
            return None

        if parser.consume().tok_type != TokenType.LAMBDA_ARROW:
            return None
        function_body = any_expression_match(parser)
        if function_body is None:
            return None

        return ArrowExpression(inputs=inputs, function_body=function_body)

    def children(self) -> list[Expression]:
        """Returns a list of child expressions."""
        return [self.inputs, self.function_body]
