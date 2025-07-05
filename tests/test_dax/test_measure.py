import pytest

from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import MeasureExpression


@pytest.mark.parametrize(
    ("input_tokens", "output"),
    [
        ([Token(TokenType.BRACKETED_IDENTIFIER, "[Total]")], "Measure ([Total])"),
    ],
)
def test_measure(input_tokens: list[Token], output: str) -> None:
    parser = Parser(input_tokens)
    result = MeasureExpression.match(parser)
    assert result is not None
    assert not parser.remaining()
    assert result.pprint() == output
