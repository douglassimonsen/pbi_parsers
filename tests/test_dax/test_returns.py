import pytest

from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import ReturnExpression


@pytest.mark.parametrize(
    ("input_tokens", "output"),
    [
        (
            [
                Token(TokenType.VARIABLE, "var"),
                Token(TokenType.UNQUOTED_IDENTIFIER, "x"),
                Token(TokenType.EQUAL_SIGN, "="),
                Token(TokenType.NUMBER_LITERAL, "42"),
                Token(TokenType.RETURN, "RETURN"),
                Token(TokenType.UNQUOTED_IDENTIFIER, "x"),
                Token(TokenType.PLUS_SIGN, "+"),
                Token(TokenType.NUMBER_LITERAL, "42"),
            ],
            """Return (
    Return: Add (
                left: Identifier (x),
                right: Number (42)
            ),
    Statements: Variable (
                    name: x,
                    statement: Number (42)
                )
)""",
        ),
    ],
)
def test_returns(input_tokens: list[Token], output: str) -> None:
    parser = Parser(input_tokens)
    result = ReturnExpression.match(parser)
    assert result is not None
    assert not parser.remaining()
    assert result.pprint() == output
