import pytest

from pbi_parsers.base.tokens import TextSlice
from pbi_parsers.dax import Parser, Token, TokenType
from pbi_parsers.dax.exprs import LiteralNumberExpression


@pytest.mark.parametrize(
    ("input_tokens", "output"),
    [
        ([Token(TokenType.NUMBER_LITERAL, TextSlice("42", 0, 2))], "Number (42)"),
        ([Token(TokenType.NUMBER_LITERAL, TextSlice("3.14", 0, 4))], "Number (3.14)"),
        (
            [
                Token(TokenType.NUMBER_LITERAL, TextSlice("1.1e1", 0, 5)),
            ],
            "Number (1.1e1)",
        ),
        (
            [
                Token(TokenType.NUMBER_LITERAL, TextSlice("-1.1e-2", 0, 7)),
            ],
            "Number (-1.1e-2)",
        ),
    ],
)
def test_literal_number(input_tokens: list[Token], output: str) -> None:
    parser = Parser(input_tokens)
    result = LiteralNumberExpression.match(parser)
    assert result is not None
    assert not parser.remaining()
    assert result.pprint() == output
