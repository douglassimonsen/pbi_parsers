import pytest

from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import KeywordExpression


@pytest.mark.parametrize(
    ("input_tokens", "output"),
    [
        ([Token(TokenType.TRUE, "TRUE")], "Keyword (TRUE)"),
        (
            [
                Token(TokenType.TRUE, "TRUE"),
                Token(TokenType.LEFT_PAREN, "("),
                Token(TokenType.RIGHT_PAREN, ")"),
            ],
            """Function (
    name: TRUE,
    args: 
)""",
        ),
        ([Token(TokenType.FALSE, "FALSE")], "Keyword (FALSE)"),
    ],
)
def test_keyword(input_tokens: list[Token], output: str) -> None:
    parser = Parser(input_tokens)
    result = KeywordExpression.match(parser)
    assert result is not None
    assert not parser.remaining()
    assert result.pprint() == output
