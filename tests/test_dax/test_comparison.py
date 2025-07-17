from pytest import mark

from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import ComparisonExpression


# TODO: Add specific test cases for ComparisonExpression
@mark.parametrize(
    ("input_tokens", "output"),
    [
        (
            [
                Token(TokenType.NUMBER_LITERAL, "1"),
                Token(TokenType.EQUAL_SIGN, "="),
                Token(TokenType.NUMBER_LITERAL, "1"),
            ],
            """Bool (
    operator: =,
    left: Number (1),
    right: Number (1)
)""",
        ),
    ],
)
def test_comparison(input_tokens: list[Token], output: str) -> None:
    parser = Parser(input_tokens)
    result = ComparisonExpression.match(parser)
    assert result is not None
    assert not parser.remaining()
    assert result.pprint() == output
