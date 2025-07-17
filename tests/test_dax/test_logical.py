import pytest

from pbi_parsers.base.tokens import TextSlice
from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import LogicalExpression


@pytest.mark.parametrize(
    ("input_tokens", "output"),
    [
        (
            [
                Token(TokenType.UNQUOTED_IDENTIFIER, TextSlice("x", 0, 1)),
                Token(TokenType.DOUBLE_AMPERSAND_OPERATOR, TextSlice("&&", 0, 2)),
                Token(TokenType.UNQUOTED_IDENTIFIER, TextSlice("y", 0, 1)),
            ],
            """Logical (
    operator: &&,
    left: Identifier (x),
    right: Identifier (y)
)""",
        ),
    ],
)
def test_logical(input_tokens: list[Token], output: str) -> None:
    parser = Parser(input_tokens)
    result = LogicalExpression.match(parser)
    assert result is not None
    assert not parser.remaining()
    assert result.pprint() == output
