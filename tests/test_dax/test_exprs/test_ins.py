import pytest

from pbi_parsers.base.tokens import TextSlice
from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import InExpression


@pytest.mark.parametrize(
    ("input_tokens", "output"),
    [
        (
            [
                Token(TokenType.UNQUOTED_IDENTIFIER, TextSlice("col", 0, 3)),
                Token(TokenType.IN, TextSlice("IN", 0, 2)),
                Token(TokenType.LEFT_PAREN, TextSlice("(", 0, 1)),
                Token(TokenType.NUMBER_LITERAL, TextSlice("1", 0, 1)),
                Token(TokenType.RIGHT_PAREN, TextSlice(")", 0, 1)),
            ],
            """In (
    value: Identifier (col),
    array: Parentheses (
               Number (1)
           )
)""",
        ),
    ],
)
def test_in(input_tokens: list[Token], output: str) -> None:
    parser = Parser(input_tokens)
    result = InExpression.match(parser)
    assert result is not None
    assert not parser.remaining()
    assert result.pprint() == output
