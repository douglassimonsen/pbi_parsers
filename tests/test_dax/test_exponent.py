import pytest

from pbi_parsers.base.tokens import TextSlice
from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import ExponentExpression


@pytest.mark.parametrize(
    ("input_tokens", "output"),
    [
        (
            [
                Token(TokenType.NUMBER_LITERAL, TextSlice("2", start=0, end=1)),
                Token(TokenType.EXPONENTIATION_SIGN, TextSlice("^", start=0, end=1)),
                Token(TokenType.NUMBER_LITERAL, TextSlice("3", start=0, end=1)),
            ],
            """Exponent (
    base: Number (2),
    power: Number (3)
)""",
        ),
    ],
)
def test_exponent(input_tokens: list[Token], output: str) -> None:
    parser = Parser(input_tokens)
    result = ExponentExpression.match(parser)
    assert result is not None
    assert not parser.remaining()
    assert result.pprint() == output
