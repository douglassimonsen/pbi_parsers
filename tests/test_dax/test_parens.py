import pytest

from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import ParenthesesExpression


@pytest.mark.parametrize(
    ("input_tokens", "output"),
    [
        (
            [Token(TokenType.LEFT_PAREN, "("), Token(TokenType.NUMBER_LITERAL, "1"), Token(TokenType.RIGHT_PAREN, ")")],
            """Parentheses (
    Number (1)
)""",
        ),
    ],
)
def test_parens(input_tokens: list[Token], output: str) -> None:
    parser = Parser(input_tokens)
    result = ParenthesesExpression.match(parser)
    assert result is not None
    assert not parser.remaining()
    assert result.pprint() == output
