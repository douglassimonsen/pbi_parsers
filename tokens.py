from enum import Enum


class TokenType(Enum):
    OPERATOR = 1
    IDENTIFIER = 2
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


class Token:
    type: TokenType
    text: str

    def __init__(self, type: TokenType, text: str):
        self.type = type
        self.text = text

    def __repr__(self):
        pretty_text = self.text.replace("\n", "\\n").replace("\r", "\\r")
        return f"Token(type={self.type.name}, text='{pretty_text}')"
