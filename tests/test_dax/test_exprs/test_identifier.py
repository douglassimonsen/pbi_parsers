import pytest

from pbi_parsers.base.tokens import TextSlice
from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import IdentifierExpression


@pytest.mark.parametrize(
    ("input_tokens", "output"),
    [
        ([Token(TokenType.UNQUOTED_IDENTIFIER, TextSlice("col", 0, 3))], "Identifier (col)"),
    ],
)
def test_identifier(input_tokens: list[Token], output: str) -> None:
    parser = Parser(input_tokens)
    result = IdentifierExpression.match(parser)
    assert result is not None
    assert not parser.remaining()
    assert result.pprint() == output
