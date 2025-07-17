import pytest

from pbi_parsers.base.tokens import TextSlice
from pbi_parsers.dax import Lexer, Token
from pbi_parsers.dax.tokens import TokenType

command1 = "1 + 2"
command2 = "func({})"


@pytest.mark.parametrize(
    ("input_str", "output"),
    [
        (
            command1,
            (
                Token(TokenType.NUMBER_LITERAL, TextSlice(command1, 0, 1)),
                Token(TokenType.WHITESPACE, TextSlice(command1, 1, 2)),
                Token(TokenType.PLUS_SIGN, TextSlice(command1, 2, 3)),
                Token(TokenType.WHITESPACE, TextSlice(command1, 3, 4)),
                Token(TokenType.NUMBER_LITERAL, TextSlice(command1, 4, 5)),
            ),
        ),
        (
            command2,
            (
                Token(TokenType.UNQUOTED_IDENTIFIER, TextSlice(command2, 0, 4)),
                Token(TokenType.LEFT_PAREN, TextSlice(command2, 4, 5)),
                Token(TokenType.LEFT_CURLY_BRACE, TextSlice(command2, 5, 6)),
                Token(TokenType.RIGHT_CURLY_BRACE, TextSlice(command2, 6, 7)),
                Token(TokenType.RIGHT_PAREN, TextSlice(command2, 7, 8)),
            ),
        ),
    ],
)
def test_lexer(input_str: str, output: tuple[Token, ...]) -> None:
    tokens = Lexer(input_str).scan()
    assert tokens == output
