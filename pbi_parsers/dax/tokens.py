from dataclasses import dataclass
from enum import Enum, auto

from pbi_parsers.base import BaseToken


class TokenType(Enum):
    AMPERSAND_OPERATOR = auto()
    ASC = auto()
    BRACKETED_IDENTIFIER = auto()
    COMMA = auto()
    COMPARISON_OPERATOR = auto()
    DESC = auto()
    DIVIDE_SIGN = auto()
    DOUBLE_AMPERSAND_OPERATOR = auto()
    DOUBLE_PIPE_OPERATOR = auto()
    EOF = auto()
    EQUAL_SIGN = auto()
    EXPONENTIATION_SIGN = auto()
    FALSE = auto()
    IN = auto()
    LEFT_CURLY_BRACE = auto()
    LEFT_PAREN = auto()
    MINUS_SIGN = auto()
    MODULUS_SIGN = auto()
    MULTIPLY_SIGN = auto()
    MULTI_LINE_COMMENT = auto()
    NOT_EQUAL_SIGN = auto()
    NUMBER_LITERAL = auto()
    PERIOD = auto()
    PLUS_SIGN = auto()
    RETURN = auto()
    RIGHT_CURLY_BRACE = auto()
    RIGHT_PAREN = auto()
    SINGLE_LINE_COMMENT = auto()
    SINGLE_QUOTED_IDENTIFIER = auto()
    STRING_LITERAL = auto()
    TRUE = auto()
    UNQUOTED_IDENTIFIER = auto()
    VARIABLE = auto()
    WHITESPACE = auto()


KEYWORD_MAPPING = {
    "TRUE": TokenType.TRUE,
    "FALSE": TokenType.FALSE,
    "ASC": TokenType.ASC,
    "DESC": TokenType.DESC,
}


@dataclass
class Token(BaseToken):
    tok_type: TokenType = TokenType.EOF
