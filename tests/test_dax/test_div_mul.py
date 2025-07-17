from pytest import mark

from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import DivMulExpression


# TODO: Add specific test cases for DivMulExpression
@mark.parametrize(
    ("input_tokens", "output"),
    [
        (
            [
                Token(TokenType.NUMBER_LITERAL, "2"),
                Token(TokenType.MULTIPLY_SIGN, "*"),
                Token(TokenType.NUMBER_LITERAL, "3"),
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
