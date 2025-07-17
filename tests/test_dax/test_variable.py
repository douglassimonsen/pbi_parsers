import pytest

from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import VariableExpression


@pytest.mark.parametrize(
    ("input_tokens", "output"),
    [
        (
            [
                Token(TokenType.VARIABLE, "var"),
                Token(TokenType.UNQUOTED_IDENTIFIER, "x"),
                Token(TokenType.EQUAL_SIGN, "="),
                Token(TokenType.NUMBER_LITERAL, "42"),
                Token(TokenType.PLUS_SIGN, "+"),
                Token(TokenType.PLUS_SIGN, "+"),
                Token(TokenType.NUMBER_LITERAL, "42"),
            ],
            """Variable (
    name: x,
    statement: Add (
                   left: Number (42),
                   right: Number (
                              sign: +,
                              number: Number (42),
                          )
               )
)""",
        ),
    ],
)
def test_variable(input_tokens: list[Token], output: str) -> None:
    parser = Parser(input_tokens)
    result = VariableExpression.match(parser)
    assert result is not None
    assert not parser.remaining()
    assert result.pprint() == output
