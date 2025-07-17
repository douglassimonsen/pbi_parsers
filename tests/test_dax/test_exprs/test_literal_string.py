import pytest

from pbi_parsers.base.tokens import TextSlice
from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import LiteralStringExpression


@pytest.mark.parametrize(
    ("input_tokens", "output"),
    [
        ([Token(TokenType.STRING_LITERAL, TextSlice("foo", 0, 3))], "String (foo)"),
    ],
)
def test_literal_string(input_tokens: list[Token], output: str) -> None:
    parser = Parser(input_tokens)
    result = LiteralStringExpression.match(parser)
    assert result is not None
    assert not parser.remaining()
    assert result.pprint() == output
