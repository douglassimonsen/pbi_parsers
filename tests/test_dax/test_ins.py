from pytest import mark

from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import InExpression


# TODO: Add specific test cases for InExpression
@mark.parametrize(
    ("input_tokens", "output"),
    [
        (
            [
                Token(TokenType.UNQUOTED_IDENTIFIER, "col"),
                Token(TokenType.IN, "IN"),
                Token(TokenType.LEFT_PAREN, "("),
                Token(TokenType.NUMBER_LITERAL, "1"),
                Token(TokenType.RIGHT_PAREN, ")"),
            ],
            """In (
    value: Identifier (col),
    array: Parentheses (
               Number (1)
           )
)""",
        ),
    ],
)
def test_in(input_tokens: list[Token], output: str) -> None:
    parser = Parser(input_tokens)
    result = InExpression.match(parser)
    assert result is not None
    assert not parser.remaining()
    assert result.pprint() == output
