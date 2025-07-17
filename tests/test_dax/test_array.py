import pytest

from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import ArrayExpression


@pytest.mark.parametrize(
    ("input_tokens", "output"),
    [
        # Example placeholder test
        (
            [
                Token(TokenType.LEFT_CURLY_BRACE, "{"),
                Token(TokenType.NUMBER_LITERAL, "1"),
                Token(TokenType.RIGHT_CURLY_BRACE, "}"),
            ],
            """Array (
    elements: Number (1)
)""",
        ),
    ],
)
def test_array(input_tokens: list[Token], output: str) -> None:
    parser = Parser(input_tokens)
    result = ArrayExpression.match(parser)
    assert result is not None
    assert not parser.remaining()
    assert result.pprint() == output
