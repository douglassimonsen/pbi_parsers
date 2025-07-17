import string

from ..base import BaseScanner
from .tokens import Token, TokenType

WHITESPACE = ["\n", "\r", "\t", " ", "\f", "\v"]
KEYWORDS = ("TRUE", "FALSE", "ASC", "DESC")


class Scanner(BaseScanner):
    def scan(self) -> list[Token]:  # type: ignore[override]
        return super().scan()  # type: ignore[override]

    def scan_helper(self) -> Token:
        start_pos: int = self.current_position

        if self.peek() == "":
            return Token(type=TokenType.EOF, text="")

        if self.match(
            "in ", case_insensitive=True
        ):  # I have found no case where "in" is not followed by a space and this allows us to avoid matching with the "int" fubction
            return Token(
                type=TokenType.IN,
                text="in",
            )

        for keyword in KEYWORDS:
            if self.match(keyword, case_insensitive=True):
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
        elif self.match("var", case_insensitive=True):
            return Token(
                type=TokenType.VARIABLE,
                text="var",
            )
        elif self.match("return", case_insensitive=True):
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
