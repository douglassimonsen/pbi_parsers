import string
from typing import Callable

from .tokens import Token, TokenType

WHITESPACE = ["\n", "\r", "\t", " ", "\f", "\v"]
KEYWORDS = ("TRUE", "FALSE", "ASC", "DESC")


class Scanner:
    source: str
    start_position: int
    current_position: int
    tokens: list[Token]

    def __init__(self, source: str):
        self.source = source
        self.start_position = 0
        self.current_position = 0
        self.tokens = []

    def match(self, matcher: Callable[[str], bool] | str, chunk: int = 1) -> bool:
        if isinstance(matcher, str):
            chunk = len(matcher)

        string_chunk = self.peek(chunk)
        if string_chunk == "":
            return False

        if isinstance(matcher, str):
            if string_chunk == matcher:
                self.advance(chunk)
                return True
            return False

        else:
            if matcher(string_chunk):
                self.advance(chunk)
                return True
            return False

    def peek(self, chunk: int = 1) -> str:
        return (
            self.source[self.current_position : self.current_position + chunk]
            if self.current_position < len(self.source)
            else str()
        )

    def remaining(self) -> str:
        return self.source[self.current_position :]

    def advance(self, chunk: int = 1) -> None:
        if self.current_position > 10000:
            raise ValueError("Current position exceeds 10000 characters.")
        self.current_position += chunk

    def scan_helper(self) -> Token:
        start_pos = self.current_position

        if self.peek() == "":
            return Token(type=TokenType.EOF, text="")

        if self.match(
            lambda c: c.lower() == "in ", chunk=3
        ):  # I have found no case where "in" is not followed by a space and this allows us to avoid matching with the "int" fubction
            return Token(
                type=TokenType.IN,
                text="in",
            )

        for keyword in KEYWORDS:
            if self.match(lambda c: c.lower() == keyword.lower(), chunk=len(keyword)):
                return Token(
                    type=TokenType.KEYWORD,
                    text=keyword,
                )

        if self.match(lambda c: c in WHITESPACE):
            while self.match(lambda c: c in WHITESPACE):
                pass
            return Token(
                type=TokenType.WHITESPACE,
                text=self.source[start_pos : self.current_position],
            )
        elif self.match(
            lambda c: c.lower() == "var", chunk=3
        ):  # need lambda for case-insensitivity
            return Token(
                type=TokenType.VARIABLE,
                text="var",
            )
        elif self.match(
            lambda c: c.lower() == "return", chunk=6
        ):  # need lambda for case-insensitivity
            return Token(
                type=TokenType.RETURN,
                text="return",
            )

        elif self.match("."):
            # must come before number literal to avoid conflict
            return Token(
                type=TokenType.PERIOD,
                text=".",
            )

        elif self.match(lambda c: c.isdigit() or c == "."):
            while self.match(lambda c: c.isdigit() or c == "."):
                pass
            return Token(
                type=TokenType.NUMBER_LITERAL,
                text=self.source[start_pos : self.current_position],
            )

        elif self.match(lambda c: c in string.ascii_letters + string.digits + "_"):
            while self.match(lambda c: c in string.ascii_letters + string.digits + "_"):
                pass
            return Token(
                type=TokenType.UNQUOTED_IDENTIFIER,
                text=self.source[start_pos : self.current_position],
            )

        elif self.match("'"):
            while self.match(lambda c: c != "'"):
                pass
            if self.match("'"):
                return Token(
                    type=TokenType.SINGLE_QUOTED_IDENTIFIER,
                    text=self.source[start_pos : self.current_position],
                )
            else:
                raise ValueError("Unterminated string literal")

        elif self.match("["):
            while self.match(lambda c: c != "]"):
                pass
            if self.match("]"):
                return Token(
                    type=TokenType.BRACKETED_IDENTIFIER,
                    text=self.source[start_pos : self.current_position],
                )
            else:
                raise ValueError("Unterminated bracketed identifier")

        elif self.match('"'):
            while self.match(lambda c: c != '"') or self.match('""'):
                pass
            if self.match('"'):
                return Token(
                    type=TokenType.STRING_LITERAL,
                    text=self.source[start_pos : self.current_position],
                )
            else:
                raise ValueError("Unterminated string literal")
        elif self.match("//") or self.match("--"):
            while self.match(lambda c: c not in ("\n", "")):
                pass
            return Token(
                type=TokenType.SINGLE_LINE_COMMENT,
                text=self.source[start_pos : self.current_position],
            )
        elif self.match("/*"):
            if self.match("*") and self.match("/"):
                return Token(
                    type=TokenType.MULTI_LINE_COMMENT,
                    text=self.source[start_pos : self.current_position],
                )
            else:
                self.advance()
            raise ValueError("Unterminated multi-line comment")

        fix_character_mapping = {
            "(": TokenType.LEFT_PAREN,
            ")": TokenType.RIGHT_PAREN,
            ",": TokenType.COMMA,
            "==": TokenType.EQUAL_SIGN,
            "=": TokenType.EQUAL_SIGN,
            "{": TokenType.LEFT_CURLY_BRACE,
            "}": TokenType.RIGHT_CURLY_BRACE,
            "<>": TokenType.EQUAL_SIGN,
            "<=": TokenType.COMPARISON_OPERATOR,
            "<": TokenType.COMPARISON_OPERATOR,
            ">=": TokenType.COMPARISON_OPERATOR,
            ">": TokenType.COMPARISON_OPERATOR,
            "||": TokenType.OPERATOR,
            "&&": TokenType.OPERATOR,
            "&": TokenType.OPERATOR,
            "+": TokenType.OPERATOR,
            "-": TokenType.OPERATOR,
            "^": TokenType.OPERATOR,
            "*": TokenType.OPERATOR,
            "%": TokenType.OPERATOR,
            "/": TokenType.OPERATOR,
        }

        for char, token_type in fix_character_mapping.items():
            if self.match(char):
                return Token(type=token_type, text=char)

        raise ValueError(
            f"Unexpected character: {self.peek()} at position {self.current_position}"
        )

    def scan(self) -> list[Token]:
        while not self.at_end():
            self.tokens.append(self.scan_helper())
        return self.tokens

    def at_end(self) -> bool:
        return self.current_position >= len(self.source)
