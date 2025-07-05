import pytest

from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import LiteralNumberExpression


@pytest.mark.parametrize(
    ("input_tokens", "output"),
    [
        ([Token(TokenType.NUMBER_LITERAL, "42")], "Number (42)"),
    ],
)
def test_literal_number(input_tokens: list[Token], output: str) -> None:
    parser = Parser(input_tokens)
    result = LiteralNumberExpression.match(parser)
    assert result is not None
    assert not parser.remaining()
    assert result.pprint() == output
