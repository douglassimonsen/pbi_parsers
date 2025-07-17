import textwrap
from typing import TYPE_CHECKING

from ..tokens import TokenType
from ._base import Expression
from ._utils import scanner_reset
from .parens import ParenthesesExpression

if TYPE_CHECKING:
    from ..parser import Parser


class ArrowExpression(Expression):
    inputs: ParenthesesExpression
    function_body: Expression

    def __init__(self, inputs: ParenthesesExpression, function_body: Expression):
        self.inputs = inputs
        self.function_body = function_body

    def pprint(self) -> str:
        inputs = textwrap.indent(self.inputs.pprint(), " " * 10)[10:]
        function_body = textwrap.indent(self.function_body.pprint(), " " * 10)[10:]
        base = f"""
Arrow (
    inputs: {inputs},
    function_body: {function_body}
)""".strip()
        return base

    @classmethod
    @scanner_reset
    def match(cls, parser: "Parser") -> "ArrowExpression | None":
        from . import any_expression_match

        inputs = ParenthesesExpression.match(parser)
        if parser.consume().type != TokenType.LAMBDA_ARROW:
            return None
        function_body = any_expression_match(parser)
        if function_body is None:
            return None

        return ArrowExpression(inputs=inputs, function_body=function_body)
