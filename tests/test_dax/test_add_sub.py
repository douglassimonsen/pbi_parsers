import pytest

from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import AddSubExpression

num1 = Token(TokenType.NUMBER_LITERAL, "1")
num2 = Token(TokenType.NUMBER_LITERAL, "2")
operator_add = Token(TokenType.PLUS_SIGN, "+")
operator_sub = Token(TokenType.MINUS_SIGN, "-")

args = [
    [
        [num1, operator_add, num2],
        """Add (
    left: Number (1),
    right: Number (2)
)""",
    ],
    [
        [num1, operator_sub, num2],
        """Sub (
    left: Number (1),
    right: Number (2)
)""",
    ],
]


@pytest.mark.parametrize(
    ("input_tokens", "output"),
    args,
)
def test_add_sub(input_tokens: list[Token], output: str) -> None:
    parser = Parser(input_tokens)
    result = AddSubExpression.match(parser)
    assert result is not None
    assert not parser.remaining()
    assert result.pprint() == output
