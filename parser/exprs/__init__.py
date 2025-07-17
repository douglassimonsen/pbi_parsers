from typing import TYPE_CHECKING

from ._base import Expression
from .add_sub import AddSubExpression
from .bool import BoolExpression
from .column import ColumnExpression
from .div_mul import DivMulExpression
from .function import FunctionExpression
from .literal_number import LiteralNumberExpression
from .literal_string import LiteralStringExpression
from .measure import MeasureExpression
from .parens import ParenthesesExpression
from .returns import ReturnExpression
from .table import TableExpression
from .variable import VariableExpression

if TYPE_CHECKING:
    from ..parser import Parser


# TODO: add ability to block expressions so the add/mult/bool hierarchy can use this as well
def any_expression_match(parser: "Parser") -> Expression | None:
    """
    Matches any expression type.
    This is a utility function to simplify the matching process in other expressions.
    """
    for expr in (
        BoolExpression,
        AddSubExpression,
        DivMulExpression,
        # The first three must stay in this order to ensure correct precedence
        ColumnExpression,
        MeasureExpression,
        FunctionExpression,
        LiteralStringExpression,
        LiteralNumberExpression,
        ParenthesesExpression,
        ReturnExpression,
        TableExpression,  # must be after ColumnExpression due to being a prefix of it. Technically, it's ambiguous with IdentifierExpression
        VariableExpression,
    ):
        if match := expr.match(parser):
            return match
    return None


__all__ = [
    "AddSubExpression",
    "ColumnExpression",
    "DivMulExpression",
    "Expression",
    "FunctionExpression",
    "LiteralNumberExpression",
    "LiteralStringExpression",
    "MeasureExpression",
    "ReturnExpression",
    "VariableExpression",
]
