import pytest

from pbi_parsers.base.tokens import TextSlice
from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import FunctionExpression


@pytest.mark.parametrize(
    ("input_tokens", "output"),
    [
        (
            [
                Token(TokenType.UNQUOTED_IDENTIFIER, TextSlice("SUM", 0, 3)),
                Token(TokenType.LEFT_PAREN, TextSlice("(", 0, 1)),
                Token(TokenType.UNQUOTED_IDENTIFIER, TextSlice("col", 0, 3)),
                Token(TokenType.RIGHT_PAREN, TextSlice(")", 0, 1)),
            ],
            """Function (
    name: SUM,
    args: Identifier (col)
)""",
        ),
    ],
)
def test_function(input_tokens: list[Token], output: str) -> None:
    parser = Parser(input_tokens)
    result = FunctionExpression.match(parser)
    assert result is not None
    assert not parser.remaining()
    assert result.pprint() == output
