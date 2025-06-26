import string
from typing import Callable

from tokens import Token, TokenType

WHITESPACE = ["\n", "\r", "\t", " ", "\f", "\v"]


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

        if self.match(lambda c: c in WHITESPACE):
            while self.match(lambda c: c in WHITESPACE):
                pass
            return Token(
                type=TokenType.WHITESPACE,
                text=self.source[start_pos : self.current_position],
            )

        elif self.match(lambda c: c in string.ascii_letters + string.digits + "_"):
            while self.match(lambda c: c in string.ascii_letters + string.digits + "_"):
                pass
            return Token(
                type=TokenType.IDENTIFIER,
                text=self.source[start_pos : self.current_position],
            )

        elif self.match("("):
            return Token(type=TokenType.LEFT_PAREN, text="(")

        elif self.match(")"):
            return Token(type=TokenType.RIGHT_PAREN, text=")")

        elif self.match(","):
            return Token(type=TokenType.COMMA, text=",")

        elif self.match("="):
            return Token(type=TokenType.EQUAL_SIGN, text="=")

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
            while self.match(lambda c: c != '"'):
                pass
            if self.match('"'):
                return Token(
                    type=TokenType.STRING_LITERAL,
                    text=self.source[start_pos : self.current_position],
                )
            else:
                raise ValueError("Unterminated string literal")
        elif self.match("//"):
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
        elif self.match(lambda c: c in "+-*%&/"):
            return Token(
                type=TokenType.OPERATOR,
                text=self.source[start_pos : self.current_position],
            )
        elif self.match(lambda c: c.isdigit() or c == "."):
            while self.match(lambda c: c.isdigit() or c == "."):
                pass
            return Token(
                type=TokenType.NUMBER_LITERAL,
                text=self.source[start_pos : self.current_position],
            )
        elif self.match("."):
            return Token(type=TokenType.PERIOD, text=".")
        elif self.match("{"):
            return Token(type=TokenType.LEFT_CURLY_BRACE, text="{")
        elif self.match("}"):
            return Token(type=TokenType.RIGHT_CURLY_BRACE, text="}")
        elif self.match("<="):
            return Token(type=TokenType.OPERATOR, text="<=")
        elif self.match("<>"):
            return Token(type=TokenType.OPERATOR, text="<>")
        elif self.match("<"):  # must be after <>, <=
            return Token(type=TokenType.OPERATOR, text="<")
        elif self.match(">="):
            return Token(type=TokenType.OPERATOR, text=">=")
        elif self.match(">"):
            return Token(type=TokenType.OPERATOR, text=">")
        elif self.match("||"):
            return Token(type=TokenType.OPERATOR, text="||")
        elif self.match("|"):
            return Token(type=TokenType.OPERATOR, text="|")
        print(self.remaining())
        breakpoint()

    def scan(self) -> None:
        while not self.at_end():
            self.tokens.append(self.scan_helper())
            print(self.tokens[-1])

    def at_end(self) -> bool:
        return self.current_position >= len(self.source)
