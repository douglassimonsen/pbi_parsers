import pytest

from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import TableExpression


@pytest.mark.parametrize(
    ("input_tokens", "output"),
    [
        (
            [Token(TokenType.UNQUOTED_IDENTIFIER, "Table")],
            """Table (
    Table
)""",
        ),
    ],
)
def test_table(input_tokens: list[Token], output: str) -> None:
    parser = Parser(input_tokens)
    result = TableExpression.match(parser)
    assert result is not None
    assert not parser.remaining()
    assert result.pprint() == output
