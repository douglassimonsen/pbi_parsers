import pytest

from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import ExponentExpression


@pytest.mark.parametrize(
    ("input_tokens", "output"),
    [
        (
            [
                Token(TokenType.NUMBER_LITERAL, "2"),
                Token(TokenType.EXPONENTIATION_SIGN, "^"),
                Token(TokenType.NUMBER_LITERAL, "3"),
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
