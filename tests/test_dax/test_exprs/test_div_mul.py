import pytest

from pbi_parsers.base.tokens import TextSlice
from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import DivMulExpression


@pytest.mark.parametrize(
    ("input_tokens", "output"),
    [
        (
            [
                Token(TokenType.NUMBER_LITERAL, TextSlice("2", start=0, end=1)),
                Token(TokenType.MULTIPLY_SIGN, TextSlice("*", start=0, end=1)),
                Token(TokenType.NUMBER_LITERAL, TextSlice("3", start=0, end=1)),
            ],
            """Mul (
    left: Number (2),
    right: Number (3)
)""",
        ),
    ],
)
def test_div_mul(input_tokens: list[Token], output: str) -> None:
    parser = Parser(input_tokens)
    result = DivMulExpression.match(parser)
    assert result is not None
    assert not parser.remaining()
    assert result.pprint() == output
