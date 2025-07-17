import string

from ..base import BaseScanner
from .tokens import Token, TokenType

WHITESPACE = ["\n", "\r", "\t", " ", "\f", "\v"]
KEYWORDS = ("null", "true", "false")


class Scanner(BaseScanner):
    def scan_helper(self) -> Token:
        start_pos: int = self.current_position

        if self.peek() == "":
            return Token(type=TokenType.EOF, text="")

        # TODO: handle as a builtin?
        for c in ("int64.type", "currency.type"):
            if self.match(c, case_insensitive=True):
                return Token(
                    type=TokenType.TYPE_LITERAL,
                    text=c,
                )

        for name, token_type in (
            ("type", TokenType.TYPE),
            ("let", TokenType.LET),
            ("if", TokenType.IF),
            ("then", TokenType.THEN),
            ("else", TokenType.ELSE),
            ("each", TokenType.EACH),
            ("meta", TokenType.META),
            ("nullable", TokenType.NULLABLE),
        ):
            if self.match(name, case_insensitive=True):
                return Token(type=token_type, text=name)

        # keywords have to be checked after the above tokens because "null" blocks "nullable"
        for keyword in KEYWORDS:
            if self.match(keyword, case_insensitive=True):
                return Token(
                    type=TokenType.KEYWORD,
                    text=keyword,
                )

        if self.match(
            lambda c: c[:2].lower() == "in" and c[2] in WHITESPACE,
            chunk=3,
        ):  # needed to handle case where "in" is followed by a newline, etc
            return Token(
                type=TokenType.IN,
                text="in",
            )

        if self.match('#"'):
            while self.match(lambda c: c != '"') or self.match('""'):
                pass
            if self.match('"'):
                return Token(
                    type=TokenType.QUOTED_IDENTIFER,
                    text=self.source[start_pos : self.current_position],
                )
            else:
                raise ValueError(
                    f"Unterminated string literal at positions: {start_pos} to {self.current_position}"
                )

        elif self.match('"'):
            while self.match(lambda c: c != '"') or self.match('""'):
                pass
            if self.match('"'):
                return Token(
                    type=TokenType.STRING_LITERAL,
                    text=self.source[start_pos : self.current_position],
                )
            else:
                raise ValueError(
                    f"Unterminated string literal at positions: {start_pos} to {self.current_position}"
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

        if self.match(lambda c: c in WHITESPACE):
            while self.match(lambda c: c in WHITESPACE):
                pass
            return Token(
                type=TokenType.WHITESPACE,
                text=self.source[start_pos : self.current_position],
            )

        elif self.match("."):
            # must come before number literal to avoid conflict
            return Token(
                type=TokenType.PERIOD,
                text=".",
            )

        elif self.match(
            lambda c: c.isdigit() or c == "."
        ):  # must come before unquoted identifier to avoid conflict
            while self.match(lambda c: c.isdigit() or c == "."):
                pass
            return Token(
                type=TokenType.NUMBER_LITERAL,
                text=self.source[start_pos : self.current_position],
            )

        elif self.match(lambda c: c.isalnum() or c == "_"):
            while self.match(lambda c: c.isalnum() or c == "_"):
                pass
            return Token(
                type=TokenType.UNQUOTED_IDENTIFIER,
                text=self.source[start_pos : self.current_position],
            )

        elif self.match("#"):
            while self.match(lambda c: c in string.ascii_letters + string.digits + "_"):
                pass
            return Token(
                type=TokenType.HASH_IDENTIFIER,
                text=self.source[start_pos : self.current_position],
            )

        fixed_character_mapping = {
            "=>": TokenType.LAMBDA_ARROW,
            ">=": TokenType.COMPARISON_OPERATOR,
            "=": TokenType.EQUAL_SIGN,
            "(": TokenType.LEFT_PAREN,
            ")": TokenType.RIGHT_PAREN,
            "{": TokenType.LEFT_CURLY_BRACE,
            "}": TokenType.RIGHT_CURLY_BRACE,
            ",": TokenType.COMMA,
            "[": TokenType.LEFT_BRACKET,
            "]": TokenType.RIGHT_BRACKET,
            "<>": TokenType.NOT_EQUAL_SIGN,
            "+": TokenType.PLUS_SIGN,
            "-": TokenType.MINUS_SIGN,
            "*": TokenType.MULTIPLY_SIGN,
            "/": TokenType.DIVIDE_SIGN,
            ">": TokenType.COMPARISON_OPERATOR,
            "&": TokenType.CONCATENATION_OPERATOR,
        }

        for char, token_type in fixed_character_mapping.items():
            if self.match(char):
                return Token(type=token_type, text=char)

        print("---------------------")
        print(self.remaining())
        print("---------------------")
        breakpoint()
        raise ValueError(
            f"Unexpected character '{self.peek()}' at position {self.current_position}"
        )
