import pytest

from pbi_parsers.base.tokens import TextSlice
from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import KeywordExpression


@pytest.mark.parametrize(
    ("input_tokens", "output"),
    [
        ([Token(TokenType.TRUE, TextSlice("TRUE", 0, 4))], "Keyword (TRUE)"),
        (
            [
                Token(TokenType.TRUE, TextSlice("TRUE", 0, 4)),
                Token(TokenType.LEFT_PAREN, TextSlice("(", 0, 1)),
                Token(TokenType.RIGHT_PAREN, TextSlice(")", 0, 1)),
            ],
            """Function (
    name: TRUE,
    args: 
)""",  # noqa: W291
        ),
        ([Token(TokenType.FALSE, TextSlice("FALSE", 0, 5))], "Keyword (FALSE)"),
    ],
)
def test_keyword(input_tokens: list[Token], output: str) -> None:
    parser = Parser(input_tokens)
    result = KeywordExpression.match(parser)
    assert result is not None
    assert not parser.remaining()
    assert result.pprint() == output
