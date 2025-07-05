from pytest import mark

from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import FunctionExpression


# TODO: Add specific test cases for FunctionExpression
@mark.parametrize(
    ("input_tokens", "output"),
    [
        (
            [
                Token(TokenType.UNQUOTED_IDENTIFIER, "SUM"),
                Token(TokenType.LEFT_PAREN, "("),
                Token(TokenType.UNQUOTED_IDENTIFIER, "col"),
                Token(TokenType.RIGHT_PAREN, ")"),
            ],
            """Function (
    name: SUM,
    args: Identifier (col)
)""",
        ),
    ],
)
def test_function(input_tokens: list[Token], output: str) -> None:
    parser = Parser(input_tokens)
    result = FunctionExpression.match(parser)
    assert result is not None
    assert not parser.remaining()
    assert result.pprint() == output
