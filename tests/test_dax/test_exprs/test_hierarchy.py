import pytest

from pbi_parsers.base.tokens import TextSlice
from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import HierarchyExpression


@pytest.mark.parametrize(
    ("input_tokens", "output"),
    [
        (
            [
                Token(TokenType.UNQUOTED_IDENTIFIER, TextSlice("Table", 0, 5)),
                Token(TokenType.BRACKETED_IDENTIFIER, TextSlice("[Column]", 0, 8)),
                Token(TokenType.PERIOD, TextSlice(".", 0, 1)),
                Token(TokenType.BRACKETED_IDENTIFIER, TextSlice("[Level]", 0, 7)),
            ],
            """Hierarchy (
    table: Table,
    column: [Column],
    level: [Level]
)""",
        ),
    ],
)
def test_hierarchy(input_tokens: list[Token], output: str) -> None:
    parser = Parser(input_tokens)
    result = HierarchyExpression.match(parser)
    assert result is not None
    assert not parser.remaining()
    assert result.pprint() == output
