import pytest

from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import ConcatenationExpression


@pytest.mark.parametrize(
    ("input_tokens", "output"),
    [
        (
            [
                Token(TokenType.STRING_LITERAL, "a"),
                Token(TokenType.AMPERSAND_OPERATOR, "&"),
                Token(TokenType.STRING_LITERAL, "b"),
            ],
            """Concat (
    left: String (a),
    right: String (b)
)""",
        ),
    ],
)
def test_concatenation(input_tokens: list[Token], output: str) -> None:
    parser = Parser(input_tokens)
    result = ConcatenationExpression.match(parser)
    assert result is not None
    assert not parser.remaining()
    assert result.pprint() == output
