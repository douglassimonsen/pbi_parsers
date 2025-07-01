from ..base import BaseToken, BaseTokenType


class TokenType(BaseTokenType):
    OPERATOR = 1
    UNQUOTED_IDENTIFIER = 2
    SINGLE_QUOTED_IDENTIFIER = 3
    BRACKETED_IDENTIFIER = 4
    STRING_LITERAL = 5
    NUMBER_LITERAL = 6
    LEFT_PAREN = 7
    RIGHT_PAREN = 8
    SINGLE_LINE_COMMENT = 9
    MULTI_LINE_COMMENT = 10
    COMMA = 11
    VARIABLE = 12
    WHITESPACE = 13
    EQUAL_SIGN = 14
    EOF = 15
    PERIOD = 16
    LEFT_CURLY_BRACE = 17
    RIGHT_CURLY_BRACE = 18
    RETURN = 19
    IN = 20
    KEYWORD = 21
    COMPARISON_OPERATOR = 22


class Token(BaseToken):
    type: TokenType  # type: ignore
    text: str

    def __init__(self, type: TokenType, text: str):
        super().__init__(type, text)
