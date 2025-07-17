import pytest

from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import ColumnExpression


@pytest.mark.parametrize(
    ("input_tokens", "output"),
    [
        (
            [Token(TokenType.UNQUOTED_IDENTIFIER, "table"), Token(TokenType.BRACKETED_IDENTIFIER, "[col]")],
            """Column (
    table,
    [col]
)""",
        ),
    ],
)
def test_column(input_tokens: list[Token], output: str) -> None:
    parser = Parser(input_tokens)
    result = ColumnExpression.match(parser)
    assert result is not None
    assert not parser.remaining()
    assert result.pprint() == output
