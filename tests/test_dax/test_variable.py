import pytest

from pbi_parsers.base.tokens import TextSlice
from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import VariableExpression


@pytest.mark.parametrize(
    ("input_tokens", "output"),
    [
        (
            [
                Token(TokenType.VARIABLE, TextSlice("var", 0, 3)),
                Token(TokenType.UNQUOTED_IDENTIFIER, TextSlice("x", 0, 1)),
                Token(TokenType.EQUAL_SIGN, TextSlice("=", 0, 1)),
                Token(TokenType.NUMBER_LITERAL, TextSlice("42", 0, 2)),
                Token(TokenType.PLUS_SIGN, TextSlice("+", 0, 1)),
                Token(TokenType.PLUS_SIGN, TextSlice("+", 0, 1)),
                Token(TokenType.NUMBER_LITERAL, TextSlice("42", 0, 2)),
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
