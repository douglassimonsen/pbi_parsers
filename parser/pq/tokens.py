from ..base import BaseToken, BaseTokenType


class TokenType(BaseTokenType):
    LET = 1
    EOF = 2
    KEYWORD = 3
    WHITESPACE = 4
    UNQUOTED_IDENTIFIER = 5
    QUOTED_IDENTIFER = 6
    EQUAL_SIGN = 7
    PERIOD = 8
    LEFT_PAREN = 9
    RIGHT_PAREN = 10
    STRING_LITERAL = 11
    LEFT_CURLY_BRACE = 12
    RIGHT_CURLY_BRACE = 13
    NUMBER_LITERAL = 14
    COMMA = 15
    LEFT_BRACKET = 16
    RIGHT_BRACKET = 17
    NOT_EQUAL_SIGN = 18
    LAMBDA_ARROW = 19
    PLUS_SIGN = 20
    MINUS_SIGN = 21
    MULTIPLY_SIGN = 22
    DIVIDE_SIGN = 23
    SINGLE_QUOTED_IDENTIFIER = 24
    HASH_IDENTIFIER = 25
    IN = 26
    TYPE = 27
    TYPE_LITERAL = 28
    COMPARISON_OPERATOR = 29
    IF = 31
    ELSE = 32
    THEN = 33
    EACH = 34
    META = 35
    CONCATENATION_OPERATOR = 36
    NULLABLE = 37
    TRY = 38
    OTHERWISE = 39
    AND = 40
    OR = 41


class Token(BaseToken):
    type: TokenType  # type: ignore
    text: str

    def __init__(self, type: TokenType, text: str):
        super().__init__(type, text)


# These are tokens that could also be used as identifiers in expressions.
TEXT_TOKENS = (
    TokenType.KEYWORD,
    TokenType.LET,
    TokenType.IN,
    TokenType.TYPE,
    TokenType.IF,
    TokenType.ELSE,
    TokenType.THEN,
    TokenType.EACH,
    TokenType.META,
    TokenType.NULLABLE,
    TokenType.TRY,
    TokenType.OTHERWISE,
)
