from pytest import mark

from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import HierarchyExpression


# TODO: Add specific test cases for HierarchyExpression
@mark.parametrize(
    ("input_tokens", "output"),
    [
        (
            [
                Token(TokenType.UNQUOTED_IDENTIFIER, "Table"),
                Token(TokenType.BRACKETED_IDENTIFIER, "[Column]"),
                Token(TokenType.PERIOD, "."),
                Token(TokenType.BRACKETED_IDENTIFIER, "[Level]"),
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
