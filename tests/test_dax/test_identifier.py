from pytest import mark

from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import IdentifierExpression


# TODO: Add specific test cases for IdentifierExpression
@mark.parametrize(
    ("input_tokens", "output"),
    [
        ([Token(TokenType.UNQUOTED_IDENTIFIER, "col")], "Identifier (col)"),
    ],
)
def test_identifier(input_tokens: list[Token], output: str) -> None:
    parser = Parser(input_tokens)
    result = IdentifierExpression.match(parser)
    assert result is not None
    assert not parser.remaining()
    assert result.pprint() == output
