from typing import TYPE_CHECKING

from ._base import Expression
from .add_sub import AddSubExpression
from .add_sub_unary import AddSubUnaryExpression
from .array import ArrayExpression
from .bool import BoolExpression
from .column import ColumnExpression
from .concatenation import ConcatenationExpression
from .div_mul import DivMulExpression
from .exponent import ExponentExpression
from .function import FunctionExpression
from .hierarchy import HierarchyExpression
from .identifier import IdentifierExpression
from .literal_number import LiteralNumberExpression
from .literal_string import LiteralStringExpression
from .logical import LogicalExpression
from .measure import MeasureExpression
from .parens import ParenthesesExpression
from .returns import ReturnExpression
from .table import TableExpression
from .variable import VariableExpression

if TYPE_CHECKING:
    from ..parser import Parser

# Bool/AddSub/DivMul must be in this order to ensure correct precedence. They must also be above all other expressions.
# Column expression must be before table and identifier expressions to ensure correct precedence.
# identifer must be before table to ensure correct precedence.

# operator precedence (https://learn.microsoft.com/en-us/dax/dax-operator-reference):
# ^ (note: the docs disagree, but I think this is correct)
# unary +,-
# *,/
# +,-
# &
# &&, || (note: this is not specified in the docs, so I'm guessing here)
# =, ==, <>, <, <=, >, >=
# NOT

EXPRESSION_HIERARCHY = (
    # Operators, must come first
    BoolExpression,
    LogicalExpression,
    ConcatenationExpression,
    AddSubExpression,
    DivMulExpression,
    ExponentExpression,
    AddSubUnaryExpression,
    # For performance, the ones with a defined prefix
    ReturnExpression,  # must come before VariableExpression
    VariableExpression,
    ParenthesesExpression,
    ArrayExpression,
    #
    FunctionExpression,
    MeasureExpression,
    #
    HierarchyExpression,
    ColumnExpression,
    IdentifierExpression,
    TableExpression,  #  Technically, it's partially ambiguous with IdentifierExpression
    #
    LiteralStringExpression,
    LiteralNumberExpression,
)


# TODO: add ability to block expressions so the add/mult/bool hierarchy can use this as well
def any_expression_match(parser: "Parser", skip_first: int = 0) -> Expression | None:
    """
    Matches any expression type.
    This is a utility function to simplify the matching process in other expressions.
    """
    for expr in EXPRESSION_HIERARCHY[skip_first:]:
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
