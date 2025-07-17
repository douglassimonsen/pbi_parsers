from pytest import mark

from pbi_parsers.dax import Expression, Token
from pbi_parsers.dax.exprs import AddSubUnaryExpression


@mark.parametrize(
    "input, output",
    [
        ("1 + 1", 2),
        ("2 - 1", 1),
        ("3 + 5", 8),
        ("10 - 2", 8),
    ],
)
def test_add_sub(input: list[Token], output: Expression):
    assert AddSubUnaryExpression  # .match(input) == output
